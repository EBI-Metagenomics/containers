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
                "RUN micromamba install -y -n base conda-forge::procps-ng",
                dockerfile,
            )
            command = run.call_args.args[0]
            self.assertEqual(command[:3], ["docker", "buildx", "build"])
            self.assertEqual(command[-1], str((root / "tools" / "1.0").resolve()))

    def test_push_requires_build(self):
        with self.assertRaisesRegex(SystemExit, "--push requires --build"):
            build.main(["bootstrap", "tools", "1.0", "--push"])


if __name__ == "__main__":
    unittest.main()
