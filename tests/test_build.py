import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build


class PackageSpecTests(unittest.TestCase):
    def test_converts_name_colon_version_to_conda_syntax(self):
        self.assertEqual(build.conda_package_spec("seqkit:2.13.0"), "seqkit=2.13.0")

    def test_preserves_existing_conda_specs(self):
        self.assertEqual(build.conda_package_spec("seqkit=2.13.0"), "seqkit=2.13.0")
        self.assertEqual(
            build.conda_package_spec("bioconda::seqkit=2.13.0"),
            "bioconda::seqkit=2.13.0",
        )


class BuildTests(unittest.TestCase):
    def test_build_can_disable_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            container = root / "tools" / "1.0"
            container.mkdir(parents=True)
            (container / "Dockerfile").write_text("FROM scratch\n")
            with patch.object(build.subprocess, "run") as run:
                self.assertEqual(
                    build.main(["build", "tools", "1.0", "--root", str(root), "--no-cache"]),
                    0,
                )

            command = run.call_args.args[0]
            self.assertIn("--no-cache", command)

    def test_build_push_can_disable_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            container = root / "tools" / "1.0"
            container.mkdir(parents=True)
            (container / "Dockerfile").write_text("FROM scratch\n")
            with patch.object(build.subprocess, "run") as run:
                self.assertEqual(
                    build.main(
                        ["build-push", "tools", "1.0", "--root", str(root), "--no-cache"]
                    ),
                    0,
                )

            command = run.call_args.args[0]
            self.assertIn("--no-cache", command)
            self.assertIn("--push", command)


class BootstrapTests(unittest.TestCase):
    def test_bootstrap_writes_multiple_packages_and_builds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(build.subprocess, "run") as run:
                self.assertEqual(
                    build.main(
                        [
                            "bootstrap",
                            "tools",
                            "1.0",
                            "--root",
                            str(root),
                            "--package",
                            "seqkit:2.13.0",
                            "--package",
                            "samtools:1.20",
                            "--build",
                        ]
                    ),
                    0,
                )

            env = (root / "tools" / "1.0" / "env.yaml").read_text()
            self.assertNotIn("procps-ng", env)
            self.assertIn("  - seqkit=2.13.0", env)
            self.assertIn("  - samtools=1.20", env)
            dockerfile = (root / "tools" / "1.0" / "Dockerfile").read_text()
            self.assertIn(
                "micromamba install -y -n base conda-forge::procps-ng",
                dockerfile,
            )
            command = run.call_args.args[0]
            self.assertEqual(command[:3], ["docker", "buildx", "build"])
            self.assertEqual(command[-1], str((root / "tools" / "1.0").resolve()))

    def test_dockerfile_sets_activation_variables(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build.main(
                ["bootstrap", "tools", "1.0", "--root", str(root), "--package", "seqkit:2.13.0"]
            )

            dockerfile = (root / "tools" / "1.0" / "Dockerfile").read_text()
            self.assertIn("USER root", dockerfile)
            self.assertIn('ENV PATH="${MAMBA_ROOT_PREFIX}/bin:${PATH}"', dockerfile)
            self.assertIn('ENV CONDA_PREFIX="${MAMBA_ROOT_PREFIX}"', dockerfile)

    @patch.object(build, "latest_version", return_value="2.13.0")
    def test_bootstrap_pins_bare_packages_to_latest(self, latest):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build.main(
                ["bootstrap", "seqkit", "2.13.0", "--root", str(root), "--package", "seqkit"]
            )

            env = (root / "seqkit" / "2.13.0" / "env.yaml").read_text()
            self.assertIn("  - seqkit=2.13.0", env)
            latest.assert_called_once_with("seqkit", "conda-forge")

    @patch.object(build, "latest_version")
    def test_bootstrap_tries_each_channel(self, latest):
        latest.side_effect = [SystemExit("not found"), "1.5.6"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build.main(["bootstrap", "mgnify-pipelines-toolkit", "1.5.6", "--root", str(root)])

            env = (root / "mgnify-pipelines-toolkit" / "1.5.6" / "env.yaml").read_text()
            self.assertIn("  - mgnify-pipelines-toolkit=1.5.6", env)
            self.assertEqual(latest.call_args.args, ("mgnify-pipelines-toolkit", "bioconda"))

    @patch.object(build, "pypi_latest_version", return_value="1.5.7")
    def test_bootstrap_pypi_writes_pip_section(self, pypi):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build.main(
                [
                    "bootstrap",
                    "mgnify-pipelines-toolkit",
                    "1.5.7",
                    "--root",
                    str(root),
                    "--pypi",
                    "--conda-package",
                    "python:3.12",
                    "--conda-package",
                    "pyfastx:2.2.0",
                ]
            )

            env = (root / "mgnify-pipelines-toolkit" / "1.5.7" / "env.yaml").read_text()
            self.assertIn(
                "  - python=3.12\n"
                "  - pyfastx=2.2.0\n"
                "  - pip\n"
                "  - pip:\n"
                "    - mgnify-pipelines-toolkit==1.5.7\n",
                env,
            )
            pypi.assert_called_once_with("mgnify-pipelines-toolkit")

    def test_conda_package_requires_pypi(self):
        with self.assertRaisesRegex(SystemExit, "--conda-package requires --pypi"):
            build.main(["bootstrap", "tools", "1.0", "--conda-package", "python"])

    def test_push_requires_build(self):
        with self.assertRaisesRegex(SystemExit, "--push requires --build"):
            build.main(["bootstrap", "tools", "1.0", "--push"])


class LatestTests(unittest.TestCase):
    @patch.object(build, "latest_version")
    @patch.object(build, "pypi_latest_version", return_value="1.5.6")
    def test_latest_can_query_pypi(self, pypi, conda):
        self.assertEqual(
            build.main(
                ["latest", "tools", "--package", "mgnify-pipelines-toolkit", "--pypi"]
            ),
            0,
        )

        pypi.assert_called_once_with("mgnify-pipelines-toolkit")
        conda.assert_not_called()


if __name__ == "__main__":
    unittest.main()
