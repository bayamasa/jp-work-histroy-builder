"""CLI entry point for jp_tenshoku_docs_builder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jp_tenshoku_docs_builder.work_history.builder import build_pdf
from jp_tenshoku_docs_builder.work_history.loader import load_yaml


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="jp_tenshoku_docs_builder",
        description="職務経歴書・履歴書 PDF Generator - Generate Japanese CV/Resume PDFs from YAML",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input YAML file path",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output/output.pdf"),
        help="Output PDF file path (default: output/output.pdf)",
    )
    parser.add_argument(
        "--font-dir",
        type=Path,
        default=None,
        help="Directory containing Japanese font files",
    )
    parser.add_argument(
        "--type",
        choices=["work-history", "resume"],
        default="work-history",
        dest="doc_type",
        help="Document type: work-history (職務経歴書) or resume (履歴書) (default: work-history)",
    )
    parser.add_argument(
        "-c", "--credential",
        type=Path,
        required=True,
        help="Path to credential YAML file containing personal info (name, address, etc.)",
    )
    parser.add_argument(
        "--format",
        choices=["standard", "star"],
        default="standard",
        dest="content_format",
        help="プロジェクト内容の表示形式 (default: standard, work-history only)",
    )
    parser.add_argument(
        "--no-split-row",
        action="store_true",
        default=False,
        help="プロジェクト行のページ途中分割を無効化（丸ごと次ページへ送る）",
    )

    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not args.credential.exists():
        print(
            f"Error: Credential file not found: {args.credential}",
            file=sys.stderr,
        )
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    if args.doc_type == "resume":
        _build_resume(args)
    else:
        _build_work_history(args)


def _build_work_history(args: argparse.Namespace) -> None:
    try:
        data = load_yaml(args.input, content_format=args.content_format, credential_path=args.credential)
    except Exception as e:
        print(
            f"Error: YAML validation failed for '{args.content_format}' format: {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        split_in_row = 0 if args.no_split_row else 1
        result = build_pdf(data, args.output, args.font_dir, content_format=args.content_format, split_in_row=split_in_row)
        print(f"Generated: {result}")
    except Exception as e:
        print(f"Error: Failed to generate PDF: {e}", file=sys.stderr)
        sys.exit(1)


def _build_resume(args: argparse.Namespace) -> None:
    from jp_tenshoku_docs_builder.resume.builder import build_resume_pdf
    from jp_tenshoku_docs_builder.resume.loader import load_resume_yaml

    try:
        data = load_resume_yaml(args.input, credential_path=args.credential)
    except Exception as e:
        print(f"Error: YAML validation failed for resume: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result = build_resume_pdf(data, args.output, args.font_dir)
        print(f"Generated: {result}")
    except Exception as e:
        print(f"Error: Failed to generate PDF: {e}", file=sys.stderr)
        sys.exit(1)
