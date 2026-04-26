# PDF Splitter

A simple command-line tool to cut multiple PDF files into segments by page range.

## Problem it solves

You have several PDF files (e.g. 30 pages each) and you want to discard some pages (e.g. pages 1–7) and keep specific ranges as separate files (e.g. pages 8–15 and pages 16–30).

## Requirements

- Python 3.10+
- [pypdf](https://pypdf.readthedocs.io/)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```
python split_pdf.py -r START-END [-r START-END ...] PDF [PDF ...]
```

### Arguments

| Argument | Description |
|---|---|
| `-r` / `--ranges` | Page range to **keep**, in `START-END` format (1-based, inclusive). Repeat the flag for each range. Pages outside every range are **discarded**. |
| `PDF` | One or more PDF files to process. |

### Examples

**Split three PDFs keeping pages 8–15 and 16–30 (discards pages 1–7):**

```bash
python split_pdf.py -r 8-15 -r 16-30 file1.pdf file2.pdf file3.pdf
```

Output files written next to the source files:

```
file1_pages_8-15.pdf    (8 pages)
file1_pages_16-30.pdf   (15 pages)
file2_pages_8-15.pdf
file2_pages_16-30.pdf
file3_pages_8-15.pdf
file3_pages_16-30.pdf
```

**Single PDF, single range:**

```bash
python split_pdf.py --ranges 5-10 report.pdf
```

## Notes

- Page numbers are **1-based** and **inclusive** on both ends, matching how PDF viewers display them.
- If a range extends beyond the last page of a PDF, it is clipped automatically with a warning.
- If a range starts beyond the last page, it is skipped with a warning.
- Original files are **never modified**.
