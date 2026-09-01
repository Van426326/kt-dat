from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "build-sing-box-rule-set.py"


class BuildSingBoxRuleSetTest(unittest.TestCase):
    def run_builder(self, source: str) -> tuple[subprocess.CompletedProcess[str], Path, tempfile.TemporaryDirectory[str]]:
        temporary_directory = tempfile.TemporaryDirectory()
        directory = Path(temporary_directory.name)
        input_path = directory / "kt.txt"
        output_path = directory / "kt.json"
        input_path.write_text(source, encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--input",
                str(input_path),
                "--output",
                str(output_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        return result, output_path, temporary_directory

    def test_builds_version_5_rule_set_with_canonical_unique_networks(self) -> None:
        result, output_path, temporary_directory = self.run_builder(
            "# comment\n192.0.2.1/24\n198.51.100.0/24\n192.0.2.0/24\n\n"
        )
        self.addCleanup(temporary_directory.cleanup)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(output_path.read_text(encoding="utf-8")),
            {
                "version": 5,
                "rules": [
                    {
                        "ip_cidr": [
                            "192.0.2.0/24",
                            "198.51.100.0/24",
                        ]
                    }
                ],
            },
        )

    def test_rejects_invalid_input_with_line_number(self) -> None:
        result, output_path, temporary_directory = self.run_builder("192.0.2.0/24\nnot-an-ip\n")
        self.addCleanup(temporary_directory.cleanup)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("line 2", result.stderr)
        self.assertFalse(output_path.exists())

    def test_rejects_empty_rule_set(self) -> None:
        result, output_path, temporary_directory = self.run_builder("# no networks\n\n")
        self.addCleanup(temporary_directory.cleanup)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no IP networks", result.stderr)
        self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
