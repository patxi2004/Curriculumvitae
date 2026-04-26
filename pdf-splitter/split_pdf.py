#!/usr/bin/env python3
"""
split_pdf.py – Split one or more PDF files into segments defined by page ranges.

Usage
-----
    python split_pdf.py --ranges 8-15 16-30 file1.pdf file2.pdf file3.pdf

Each PDF is split into one output file per range.  Pages outside every range
are discarded.  Output files are written next to the source file with a suffix
that reflects the range, e.g.:

    file1_pages_8-15.pdf
    file1_pages_16-30.pdf

Page numbers are 1-based and inclusive on both ends, matching how a PDF viewer
shows them.
"""

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def parse_range(range_str: str) -> tuple[int, int]:
    """Parse a '8-15' string into a (start, end) tuple (1-based, inclusive)."""
    parts = range_str.split("-")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            f"Invalid range '{range_str}'. Expected format: START-END (e.g. 8-15)"
        )
    try:
        start, end = int(parts[0]), int(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid range '{range_str}'. START and END must be integers."
        )
    if start < 1:
        raise argparse.ArgumentTypeError(
            f"Invalid range '{range_str}'. Page numbers must be >= 1."
        )
    if start > end:
        raise argparse.ArgumentTypeError(
            f"Invalid range '{range_str}'. START must be <= END."
        )
    return start, end


def split_pdf(pdf_path: Path, ranges: list[tuple[int, int]]) -> None:
    """Extract each range from *pdf_path* and write a separate output file."""
    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)

    for start, end in ranges:
        if start > total_pages:
            print(
                f"  WARNING: range {start}-{end} starts beyond the last page "
                f"({total_pages}) in '{pdf_path.name}'. Skipping.",
                file=sys.stderr,
            )
            continue

        actual_end = min(end, total_pages)
        if actual_end < end:
            print(
                f"  WARNING: range {start}-{end} clipped to {start}-{actual_end} "
                f"('{pdf_path.name}' has only {total_pages} pages).",
                file=sys.stderr,
            )

        writer = PdfWriter()
        for page_num in range(start - 1, actual_end):  # convert to 0-based index
            writer.add_page(reader.pages[page_num])

        suffix = f"_pages_{start}-{actual_end}"
        output_path = pdf_path.with_name(pdf_path.stem + suffix + pdf_path.suffix)
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"  Wrote {len(writer.pages)} pages -> {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Split one or more PDF files into segments defined by page ranges. "
            "Pages outside every range are discarded."
        )
    )
    parser.add_argument(
        "--ranges",
        "-r",
        metavar="START-END",
        action="append",
        required=True,
        help=(
            "Page range to keep, e.g. -r 8-15 -r 16-30. "
            "Repeat the flag for each range. "
            "Page numbers are 1-based and inclusive."
        ),
    )
    parser.add_argument(
        "pdfs",
        metavar="PDF",
        nargs="+",
        help="One or more PDF files to process.",
    )

    args = parser.parse_args()

    try:
        ranges = [parse_range(r) for r in args.ranges]
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))

    for pdf_file in args.pdfs:
        path = Path(pdf_file)
        if not path.is_file():
            print(f"ERROR: '{pdf_file}' not found or is not a file.", file=sys.stderr)
            sys.exit(1)
        if path.suffix.lower() != ".pdf":
            print(f"WARNING: '{pdf_file}' does not have a .pdf extension.", file=sys.stderr)

        print(f"Processing '{path.name}' ({len(PdfReader(str(path)).pages)} pages)…")
        split_pdf(path, ranges)


if __name__ == "__main__":
    main()
