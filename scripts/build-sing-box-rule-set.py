#!/usr/bin/env python3
"""Convert a plaintext IP/CIDR list into a sing-box source rule-set."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import sys
import tempfile
from pathlib import Path

RULE_SET_VERSION = 5


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="plaintext IP/CIDR input")
    parser.add_argument("--output", type=Path, required=True, help="sing-box source JSON output")
    return parser.parse_args()


def load_networks(path: Path) -> list[str]:
    networks: list[str] = []
    seen: set[str] = set()
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        value = raw_line.strip()
        if not value or value.startswith("#"):
            continue
        try:
            network = str(ipaddress.ip_network(value, strict=False))
        except ValueError as exc:
            raise ValueError(f"invalid IP network on line {line_number}: {value!r}") from exc
        if network not in seen:
            seen.add(network)
            networks.append(network)
    if not networks:
        raise ValueError("input contains no IP networks")
    return networks


def write_rule_set(path: Path, networks: list[str]) -> None:
    document = {
        "version": RULE_SET_VERSION,
        "rules": [
            {
                "ip_cidr": networks,
            }
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as output_file:
            json.dump(document, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def main() -> int:
    arguments = parse_arguments()
    try:
        networks = load_networks(arguments.input)
        write_rule_set(arguments.output, networks)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Generated {arguments.output} with {len(networks)} unique IP networks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
