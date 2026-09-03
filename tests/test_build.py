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
            self.assertIn("  - conda-forge::procps-ng", env)
            self.assertIn("  - seqkit=2.13.0", env)
            self.assertIn("  - samtools=1.20", env)
            command = run.call_args.args[0]
            self.assertEqual(command[:3], ["docker", "buildx", "build"])
            self.assertEqual(command[-1], str((root / "tools" / "1.0").resolve()))

    def test_push_requires_build(self):
        with self.assertRaisesRegex(SystemExit, "--push requires --build"):
            build.main(["bootstrap", "tools", "1.0", "--push"])


if __name__ == "__main__":
    unittest.main()
