#!/usr/bin/env python3
"""Build and maintain micromamba-based container definitions."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from string import Template
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

DEFAULT_REGISTRY = "quay.io/microbiome-informatics"
DEFAULT_PLATFORMS = "linux/arm64,linux/amd64"
DEFAULT_BASE_IMAGE = "mambaorg/micromamba:2.9.0"
GIT_VERSION_LENGTH = 7
ENVIRONMENT_FILES = (
    "Dockerfile",
    "env.yaml",
    "env.yml",
    "environment.yaml",
    "environment.yml",
    "environment.lock",
)

DOCKERFILE_TEMPLATE = Template('''FROM ${base_image}

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL software="${tool}"
LABEL software.version="${version}"

COPY --chown=$${MAMBA_USER}:$${MAMBA_USER} env.yaml /tmp/env.yaml

RUN micromamba install -y -n base -f /tmp/env.yaml \\
    && micromamba install -y -n base conda-forge::procps-ng \\
    && micromamba clean --all --yes \\
    && rm /tmp/env.yaml

ENV PATH="$${MAMBA_ROOT_PREFIX}/bin:$${PATH}"
''')

GIT_DOCKERFILE_TEMPLATE = Template('''FROM ${base_image}

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL software="${tool}"
LABEL software.version="${version}"

COPY --chown=$${MAMBA_USER}:$${MAMBA_USER} env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml \\
    && micromamba clean --all --yes \\
    && rm /tmp/env.yaml

ARG MAMBA_DOCKERFILE_ACTIVATE=1  # (otherwise python will not be found)

# Git source: ${git_url} (requested ref: ${git_ref}, resolved commit: ${version})
RUN python -m pip install --no-cache-dir git+${git_url}@${sha}

RUN micromamba install -y -n base conda-forge::procps-ng

WORKDIR /data
CMD ["/bin/bash", "-c"]
''')

ENV_TEMPLATE = Template('''name: base
channels:
${channels}
dependencies:
${dependencies}
''')

GIT_SOURCE_PATTERN = re.compile(r"git\+([^\s\"']+?)(?:@([^\s\"']+))?(?=\s|$)")
PACKAGE_VERSION_PATTERN = re.compile(r"^(?P<name>[^:=\s]+):(?P<version>[^:\s]+)$")


def container_dir(root: Path, tool: str, version: str) -> Path:
    """Return the versioned container directory after validating its names."""
    if not tool or "/" in tool or tool in {".", ".."}:
        raise ValueError("tool must be a non-empty directory name")
    if not version or "/" in version or version in {".", ".."}:
        raise ValueError("version must be a non-empty directory name")
    return root / tool / version


def require_dockerfile(path: Path) -> None:
    """Stop with a clear error unless ``path`` contains a Dockerfile."""
    if not path.is_dir():
        raise SystemExit(f"Container directory does not exist: {path}")
    if not (path / "Dockerfile").is_file():
        raise SystemExit(f"Dockerfile not found: {path / 'Dockerfile'}")


def run_build(args: argparse.Namespace, root: Path) -> int:
    """Build the selected container image, optionally pushing it to a registry."""
    path = container_dir(root, args.tool, args.version)
    require_dockerfile(path)
    image = f"{args.registry.rstrip('/')}/{args.tool}:{args.version}"
    command = [
        "docker", "buildx", "build", "--platform", args.platforms,
        "--tag", image,
    ]
    if getattr(args, "no_cache", False):
        command.append("--no-cache")
    if args.push:
        command.append("--push")
    command.append(str(path))
    print("+", shlex.join(command))
    subprocess.run(command, check=True)
    return 0


def list_containers(root: Path) -> int:
    """Print tools and their version directories beneath ``root``."""
    for tool_dir in sorted(root.iterdir()):
        if not tool_dir.is_dir() or tool_dir.name.startswith("."):
            continue
        versions = sorted(
            version.name
            for version in tool_dir.iterdir()
            if version.is_dir() and (version / "Dockerfile").is_file()
        )
        if versions:
            print(f"{tool_dir.name}:")
            for version in versions:
                print(f"  {version}")
    return 0


def yaml_items(items: list[str], indent: int = 2) -> str:
    """Render strings as a simple indented YAML list."""
    prefix = " " * indent
    return "\n".join(f"{prefix}- {item}" for item in items)


def conda_package_spec(package: str) -> str:
    """Accept ``name:version`` shorthand and return Conda's ``name=version`` form."""
    match = PACKAGE_VERSION_PATTERN.fullmatch(package)
    if match is None:
        return package
    return f"{match.group('name')}={match.group('version')}"


def github_repo(url: str) -> tuple[str, str]:
    """Extract an owner and repository from a supported HTTPS GitHub URL."""
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
        raise SystemExit(
            f"Unsupported GitHub URL: {url} "
            "(use https://github.com/OWNER/REPOSITORY)"
        )
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) != 2 or parsed.query or parsed.fragment:
        raise SystemExit(
            f"Unsupported GitHub URL: {url} "
            "(use https://github.com/OWNER/REPOSITORY)"
        )
    return parts[0], parts[1].removesuffix(".git")


def resolve_git_ref(url: str, ref: str) -> str:
    """Resolve a GitHub branch, tag, or SHA to a 40-character commit SHA."""
    owner, repository = github_repo(url)
    endpoint = (
        f"https://api.github.com/repos/{quote(owner, safe='')}/"
        f"{quote(repository, safe='')}/commits/{quote(ref, safe='')}"
    )
    request = Request(
        endpoint,
        headers={
            "User-Agent": "containers-build.py/1.0",
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            data = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise SystemExit(
                f"GitHub repository or ref not found: {url}@{ref}"
            ) from error
        raise SystemExit(
            f"Could not query GitHub for {url}@{ref}: HTTP {error.code}"
        ) from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise SystemExit(f"Could not query GitHub for {url}@{ref}: {error}") from error
    sha = data.get("sha")
    valid_sha = (
        isinstance(sha, str)
        and len(sha) == 40
        and all(char in "0123456789abcdefABCDEF" for char in sha)
    )
    if not valid_sha:
        raise SystemExit(f"GitHub returned no valid commit SHA for {url}@{ref}")
    return sha.lower()


def short_git_sha(sha: str) -> str:
    """Return the abbreviated SHA used for Git container versions."""
    return sha[:GIT_VERSION_LENGTH]


def detected_git_source(dockerfile: Path) -> tuple[str | None, str | None]:
    """Find the first ``git+URL[@ref]`` source in a Dockerfile."""
    text = dockerfile.read_text()
    match = GIT_SOURCE_PATTERN.search(text)
    if match is None:
        return None, None
    return match.group(1), match.group(2)


def git_source(
    args: argparse.Namespace, source: Path | None = None
) -> tuple[str, str]:
    """Combine explicit Git options with source metadata detected from a Dockerfile."""
    detected_url = detected_ref = None
    if source is not None:
        detected_url, detected_ref = detected_git_source(source / "Dockerfile")
    url = args.git_url or detected_url
    ref = args.git_ref or detected_ref or "main"
    if not url:
        raise SystemExit(
            "Git source is unresolved: provide --git-url or use a Dockerfile "
            "with a git+URL source"
        )
    github_repo(url)
    return url, ref


def write_container(
    path: Path,
    args: argparse.Namespace,
    version: str,
    git_url: str | None = None,
    git_ref: str | None = None,
    sha: str | None = None,
) -> None:
    """Write a Dockerfile and environment file for conda or Git installation."""
    path.mkdir(parents=True, exist_ok=True)
    packages = [
        *(conda_package_spec(package) for package in (args.package or [args.tool])),
    ]
    channels = args.channel or ["conda-forge", "bioconda"]
    if git_url:
        packages = ["git", "python", "pip", *packages]
        dockerfile = GIT_DOCKERFILE_TEMPLATE.substitute(
            base_image=args.base_image,
            tool=args.tool,
            version=version,
            git_url=git_url,
            git_ref=git_ref,
            sha=sha,
        )
    else:
        dockerfile = DOCKERFILE_TEMPLATE.substitute(
            base_image=args.base_image,
            tool=args.tool,
            version=version,
        )
    (path / "Dockerfile").write_text(dockerfile)
    (path / "env.yaml").write_text(
        ENV_TEMPLATE.substitute(
            channels=yaml_items(channels),
            dependencies=yaml_items(packages),
        )
    )


def bootstrap(args: argparse.Namespace, root: Path) -> int:
    """Create a container definition and optionally build its image."""
    if args.push and not args.build:
        raise SystemExit("--push requires --build")
    git_url = None
    git_ref = None
    sha = None
    if args.git_url:
        git_url, git_ref = git_source(args)
        sha = resolve_git_ref(git_url, git_ref)
    version = short_git_sha(sha) if sha else args.version
    path = container_dir(root, args.tool, version)
    if path.exists() and any(path.iterdir()) and not args.force:
        raise SystemExit(
            f"Refusing to overwrite non-empty directory: {path} (use --force)"
        )
    write_container(path, args, version, git_url, git_ref, sha)
    print(f"Created {path / 'Dockerfile'}")
    print(f"Created {path / 'env.yaml'}")
    if args.build:
        args.version = version
        run_build(args, root)
    return 0


def latest_version(package: str, channel: str) -> str:
    """Query Bioconda for the latest version of a package in a channel."""
    url = f"https://api.anaconda.org/package/{quote(channel)}/{quote(package)}"
    request = Request(url, headers={"User-Agent": "containers-build.py/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            data = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise SystemExit(f"Could not query {channel}/{package}: {error}") from error
    version = data.get("latest_version")
    if not version:
        raise SystemExit(f"No latest version reported for {channel}/{package}")
    return version


def show_latest(args: argparse.Namespace) -> int:
    """Print the latest conda version or resolved Git commit for a tool."""
    if args.git_url:
        ref = args.git_ref or "main"
        sha = resolve_git_ref(args.git_url, ref)
        print(f"{args.git_url}@{ref}: {short_git_sha(sha)}")
        return 0
    package = args.package or args.tool
    version = latest_version(package, args.channel)
    print(f"{args.channel}/{package}: {version}")
    return 0


def update(args: argparse.Namespace, root: Path) -> int:
    """Copy a container definition to its next conda version or Git commit."""
    source = container_dir(root, args.tool, args.version)
    require_dockerfile(source)
    if args.git_url or args.git_ref or detected_git_source(source / "Dockerfile")[0]:
        git_url, git_ref = git_source(args, source)
        new_sha = resolve_git_ref(git_url, git_ref)
        new_version = short_git_sha(new_sha)
        package = None
    else:
        git_url = git_ref = None
        package = args.package or args.tool
        new_version = latest_version(package, args.channel)
    destination = container_dir(root, args.tool, new_version)
    source_label = f"{git_url}@{git_ref}" if git_url else f"{args.channel}/{package}"
    if new_version == args.version:
        print(f"{source_label} is already at {args.version}")
        return 0
    print(f"{args.tool}: {args.version} -> {new_version} ({source_label})")
    if not args.yes:
        confirmation = input("Create the updated container directory? [y/N] ")
        if confirmation.lower() not in {"y", "yes"}:
            print("Cancelled")
            return 0
    if destination.exists():
        if not args.force:
            raise SystemExit(
                f"Refusing to overwrite existing directory: {destination} "
                "(use --force)"
            )
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    if git_url:
        dockerfile = destination / "Dockerfile"
        text = dockerfile.read_text()
        text = text.replace(args.version, new_version)
        text = re.sub(r"git\+[^\s\"']+", f"git+{git_url}@{new_sha}", text, count=1)
        dockerfile.write_text(text)
    for filename in ENVIRONMENT_FILES:
        if git_url and filename == "Dockerfile":
            continue
        path = destination / filename
        if path.is_file():
            text = path.read_text()
            path.write_text(text.replace(args.version, new_version))
    print(f"Created {destination}")
    print("Review the Dockerfile and environment pins, then build it with:")
    print(f"  {Path(__file__).name} build {args.tool} {new_version}")
    return 0


def parser() -> argparse.ArgumentParser:
    """Create the command-line parser for all supported operations."""
    root_common = argparse.ArgumentParser(add_help=False)
    root_common.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    root_common.add_argument(
        "--registry",
        default=os.environ.get("CONTAINER_REGISTRY", DEFAULT_REGISTRY),
    )
    root_common.add_argument(
        "--platforms",
        default=os.environ.get("CONTAINER_PLATFORMS", DEFAULT_PLATFORMS),
    )
    sub_common = argparse.ArgumentParser(add_help=False)
    sub_common.add_argument("--root", type=Path, default=argparse.SUPPRESS)
    sub_common.add_argument("--registry", default=argparse.SUPPRESS)
    sub_common.add_argument("--platforms", default=argparse.SUPPRESS)
    command_parser = argparse.ArgumentParser(description=__doc__, parents=[root_common])
    subparsers = command_parser.add_subparsers(dest="command", required=True)
    for name, push in (("build", False), ("build-push", True)):
        subparser = subparsers.add_parser(
            name, parents=[sub_common], help="build a container image"
        )
        subparser.add_argument("tool")
        subparser.add_argument("version")
        subparser.add_argument(
            "--no-cache", action="store_true",
            help="build the image without using the Docker build cache",
        )
        subparser.set_defaults(push=push)
    subparsers.add_parser("list", parents=[sub_common], help="list versioned containers")
    subparser = subparsers.add_parser(
        "latest", parents=[sub_common], help="query the latest package version"
    )
    subparser.add_argument("tool")
    subparser.add_argument("--package", help="package name (defaults to TOOL)")
    subparser.add_argument("--channel", default="bioconda")
    subparser.add_argument("--git-url", help="pip-installable GitHub repository URL")
    subparser.add_argument("--git-ref", help="GitHub branch or tag (defaults to main)")
    subparser = subparsers.add_parser(
        "bootstrap", parents=[sub_common], help="create a micromamba container"
    )
    subparser.add_argument("tool")
    subparser.add_argument("version")
    subparser.add_argument(
        "--package", action="append",
        help="conda package, optionally NAME:VERSION (repeatable; defaults to TOOL)",
    )
    subparser.add_argument("--channel", action="append", help="conda channel (repeatable)")
    subparser.add_argument("--base-image", default=DEFAULT_BASE_IMAGE)
    subparser.add_argument("--git-url", help="pip-installable GitHub repository URL")
    subparser.add_argument("--git-ref", help="GitHub branch or tag (defaults to main)")
    subparser.add_argument(
        "--force", action="store_true", help="overwrite files in an existing directory"
    )
    subparser.add_argument(
        "--build", action="store_true", help="build the image after creating the definition"
    )
    subparser.add_argument(
        "--push", action="store_true", help="push the image when used with --build"
    )
    subparser = subparsers.add_parser(
        "update", parents=[sub_common], help="copy a container using a latest package version"
    )
    subparser.add_argument("tool")
    subparser.add_argument("version", help="existing container version to update")
    subparser.add_argument("--package", help="package name (defaults to TOOL)")
    subparser.add_argument("--channel", default="bioconda")
    subparser.add_argument("--git-url", help="pip-installable GitHub repository URL")
    subparser.add_argument("--git-ref", help="GitHub branch or tag (defaults to main)")
    subparser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    subparser.add_argument(
        "--force", action="store_true", help="replace an existing target version"
    )
    return command_parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, dispatch the command, and translate expected failures."""
    args = parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command in {"build", "build-push"}:
            return run_build(args, root)
        if args.command == "list":
            return list_containers(root)
        if args.command == "latest":
            return show_latest(args)
        if args.command == "bootstrap":
            return bootstrap(args, root)
        return update(args, root)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    except subprocess.CalledProcessError as error:
        return error.returncode


if __name__ == "__main__":
    sys.exit(main())
