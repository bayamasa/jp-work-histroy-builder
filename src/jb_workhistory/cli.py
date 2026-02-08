"""CLI entry point for jb_workhistory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jb_workhistory.builder import build_pdf
from jb_workhistory.loader import load_yaml


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="jb_workhistory",
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
    parser.add_argument(
        "--format",
        choices=["standard", "star"],
        default="standard",
        dest="content_format",
        help="プロジェクト内容の表示形式 (default: standard)",
    )

    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        data = load_yaml(args.input, content_format=args.content_format)
    except Exception as e:
        print(
            f"Error: YAML validation failed for '{args.content_format}' format: {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = build_pdf(data, args.output, args.font_dir, content_format=args.content_format)
        print(f"Generated: {result}")
    except Exception as e:
        print(f"Error: Failed to generate PDF: {e}", file=sys.stderr)
        sys.exit(1)
