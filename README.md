# Container images

This repository contains container definitions used by the Microbiome Informatics Team at EMBL-EBI. Each container is kept in a tool/version directory containing a `Dockerfile` and, where applicable, an environment file.

## Requirements

- Python 3.9 or newer
- Docker with Buildx support
- Internet access for `latest`, Git-based `bootstrap`, and `update` operations

## Build images

Use `build.py` to build a container for a tool and version:

```bash
./build.py build interproscan 5.76-107.0_patch1
```

Images are tagged in the default registry as `quay.io/microbiome-informatics/TOOL:VERSION` and built for `linux/arm64,linux/amd64` by default.

To build and push an image to quay.io:

```bash
./build.py build-push interproscan 5.76-107.0_patch1
```

You must be authenticated to the `quay.io/microbiome-informatics` organization before pushing.

The registry, platforms, and repository root can be changed with options or environment variables:

```bash
CONTAINER_REGISTRY=quay.io/example \
CONTAINER_PLATFORMS=linux/amd64 \
./build.py build --root . interproscan 5.76-107.0_patch1
```

Run `./build.py --help` or `./build.py COMMAND --help` for all options.

## Manage container definitions

List all versioned containers:

```bash
./build.py list
```

Create a micromamba-based definition from a conda package:

```bash
./build.py bootstrap my-tool 1.2.3 --package package-name
```

A pip-installable Python package can be built from a GitHub repository when it is not available as a conda package. The repository must support installation through `pip install git+URL`; this Git source option is not intended for arbitrary repositories. The branch or tag is resolved to a commit SHA. Its first seven characters become the directory version; the generated Dockerfile retains the full SHA for an exact source pin:

```bash
./build.py bootstrap gemsparcl main \
  --git-url https://github.com/johannahelene/gemsparcl \
  --git-ref main
```

Query the latest conda package version or resolve a GitHub ref:

```bash
./build.py latest interproscan
./build.py latest gemsparcl \
  --git-url https://github.com/johannahelene/gemsparcl \
  --git-ref main
```

Copy an existing definition to the latest package version or Git commit:

```bash
./build.py update interproscan 5.76-107.0_patch1 --yes
```

Review generated or updated files before building them. Existing non-empty destinations are protected unless `--force` is supplied.

## Repository layout

```text
tool-name/
└── version/
    ├── Dockerfile
    └── env.yaml
```

Images are published under the [`microbiome-informatics` Quay.io organization](https://quay.io/repository/microbiome-informatics).
