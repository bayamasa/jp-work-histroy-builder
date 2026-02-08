"""CLI entry point for jpcv."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jpcv.builder import build_pdf
from jpcv.loader import load_yaml


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="jpcv",
        description="職務経歴書 PDF Generator - Generate Japanese work history PDFs from YAML",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input YAML file path",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output.pdf"),
        help="Output PDF file path (default: output.pdf)",
    )
    parser.add_argument(
        "--font-dir",
        type=Path,
        default=None,
        help="Directory containing Japanese font files",
    )

    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        data = load_yaml(args.input)
    except Exception as e:
        print(f"Error: Failed to load YAML: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result = build_pdf(data, args.output, args.font_dir)
        print(f"Generated: {result}")
    except Exception as e:
        print(f"Error: Failed to generate PDF: {e}", file=sys.stderr)
        sys.exit(1)
