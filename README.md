# PDF Reader CLI – Documentation

A lightweight command‑line application to **read** PDF text directly to the terminal and to **merge** multiple PDF files into a single output file.

---

## Table of Contents

* [Overview](#overview)
* [System Requirements](#system-requirements)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [CLI Reference](#cli-reference)

  * [`read` – Read a PDF](#read--read-a-pdf)
  * [`merge` – Merge PDFs](#merge--merge-pdfs)
  * [`convert` – Convert PDFs](#convert--convert-pdfs)
* [Examples](#examples)
* [Exit Codes](#exit-codes)
* [Error Handling & Troubleshooting](#error-handling--troubleshooting)
* [Architecture & Code Overview](#architecture--code-overview)

  * [Module `cli.py`](#module-clipy)
  * [Module `core.py` (Expected API)](#module-corepy-expected-api)
* [Development](#development)
* [Tests & Quality Assurance](#tests--quality-assurance)
* [Packaging (optional)](#packaging-optional)
* [Versioning & Releases](#versioning--releases)
* [Contributing](#contributing)
* [Security](#security)
* [License](#license)
* [FAQ](#faq)

---

## Overview

This CLI provides two main features:

* **`read`**: Reads a PDF file and prints the extracted text to `stdout` (visible in the terminal). Optionally, you can specify page ranges and a password.
* **`merge`**: Merges two or more PDF files in the order provided into a single output file.

The program name in the parser is set to `PDF_reader`.

---

## System Requirements

* **Python**: 3.9 or newer
* Operating systems: Linux, macOS, Windows
* Dependencies: See `pyproject.toml`.

---

## Installation

### From Source (direct invocation)

```bash
git clone https://github.com/Kamillendampf/Free-PDF-Tool
cd Free-PDF-Tool
pipx install . #installs the software and add it to PATH

```

You can then invoke the CLI directly via Python:

```bash
python cli.py read -f ./docs/report.pdf
python cli.py merge -o ./out/combined.pdf -i ./a.pdf ./b.pdf
```

After installation, you can call the tool as a command (name depends on the entry point), e.g., `pdfreader`.

---

## Quick Start

```bash
# Read a PDF
pdfreader read -f ./docs/report.pdf

# Read specific pages
pdfreader read -f ./docs/report.pdf -p 1-3,7

# Merge PDFs (order is respected)
pdfreader merge -o ./out/combined.pdf -i ./in/a.pdf ./in/b.pdf ./in/c.pdf
```

---

## CLI Reference

### Global Structure

```
PDF_reader [COMMAND] [OPTIONS]
```

### `read` – Read a PDF

Reads a PDF file and prints its text to `stdout`.

**Options**

* `-f, --file <PATH>` – Input file (PDF)
* `-p, --pages <RANGE>` – Page range (e.g., `1-3,5,10-13`; default: all)
* `-pass, --password <PW>` – Password for encrypted PDFs (if supported)

**Notes for `--pages`**

* **Ranges**: `a-b` (from `a` to `b`, inclusive)
* **Single page**: `7` (only page 7)
* **Combinations**: separate with commas, e.g., `1-3,5,10-13`

**Example**

```bash
pdfreader read -f ./docs/report.pdf -p 1-3,5,10-13
```

### `merge` – Merge PDFs

Merges two or more PDFs into a single file.

**Options**

* `-o, --output <PATH>` – Output file (e.g., `./out/combined.pdf`)
* `-i, --input <FILES...>` – List of input files in merge order

**Example**

```bash
pdfreader merge -o ./out/combined.pdf -i ./in/a.pdf ./in/b.pdf ./in/c.pdf
```

> **Note:** In the current parser, `--output` and `--input` are not marked as *required*. If they are missing, `core.merge_pdf` will likely raise an error. In practice, always provide both options.

---

### `convert` – Convert PDFs

Convert one PDF int to a docx file.

**Options**
* `-o, --output <PATH>` – Output file (e.g., `./out/combined.pdf`)
* `-i, --input <FILES...>` – List of input files in merge order
* `-p, --pages <RANGE>` – Page range (e.g., `1-3,5,10-13`; default: all)
* `-pass, --password <PW>` – Password for encrypted PDFs (if supported)

**Notes for `--pages`**

* **Ranges**: `a-b` (from `a` to `b`, inclusive)
* **Single page**: `7` (only page 7)
* **Combinations**: separate with commas, e.g., `1-3,5,10-13`



## Examples

```bash
# 1) Print the text of a PDF
pdfreader read -f ./docs/report.pdf

# 2) Read only specific pages
pdfreader read -f ./docs/report.pdf -p 1-3,7

# 3) Read a password-protected file
pdfreader read -f ./docs/secret.pdf -pass "topsecret"

# 4) Merge multiple PDFs
pdfreader merge -o ./out/merged.pdf -i ./in/a.pdf ./in/b.pdf

# 5) Redirect output to a text file
pdfreader read -f ./docs/report.pdf > ./out/report.txt
```

---

## Exit Codes

* `0` – Success
* `1` – Error in the merge handler (exceptions are caught and printed to `stderr`)

> The `read` handler currently always returns `0`. For consistent behavior, you may add a `try/except` similar to the merge handler.

---

## Error Handling & Troubleshooting

**General**

* Check paths and file permissions for input files.
* Ensure the output file can be written (directory exists, write permissions available, file not locked).

**Common Cases**

* *`FileNotFoundError`*: Correct the path; try absolute paths.
* *`PermissionError`*: Verify read/write rights; choose a different output directory if needed.
* *Empty output when reading*: The PDF may contain only scanned images without OCR.
* *Password errors*: Double-check the password; some backends are case-sensitive and may not support all encryption variants.

**Debugging Tips**

* Temporarily add extra logging in `core.read_pdf`/`core.merge_pdf`.
* Isolate the problematic file and document a minimal reproduction/stack trace.

---

## Architecture & Code Overview

### Module `cli.py`

* Argument parsing via `argparse`
* Subcommands: `read`, `merge`
* Dispatch using `set_defaults(func=...)` → `args.func(args)`
* `handle_merge(args)`: Calls `core.merge_pdf(output, input_list)`, catches exceptions, prints status to `stderr/stdout`, and returns `0/1`.
* `handle_reader(args)`: Calls `core.read_pdf(file, pages, password)` and prints the result.

### Module `core.py` (Expected API)

The CLI calls the following functions. Example signatures inferred from usage:

```python
def merge_pdf(output_path: str, input_files: list[str]) -> None:
    """Merge the files in `input_files` in the given order into `output_path`."""


def read_pdf(file_path: str, pages: str | None, password: str | None) -> str:
    """Read text from `file_path`. Optional page range `pages` (e.g., "1-3,5") and `password`.
    Returns the extracted text (printed to stdout by the CLI)."""
```

> The concrete implementation (parsing page ranges, PDF backend, error classes) lives in `core.py`.

---

## Development

### Suggested Project Structure

```
.
├── core.py            # Implementation of read_pdf / merge_pdf
├── cli.py             # Argument parsing & subcommands
├── tests/             # Unit & integration tests (recommended)
├── README.md
└── pyproject.toml / requirements.txt
```

### Local Execution

```bash
python main.py read -f ./sample.pdf
python main.py merge -o ./out.pdf -i ./a.pdf ./b.pdf
```

### Code Style

* PEP 8 (snake_case, max line length 88/120)
* Type hints (PEP 484)
* Descriptive names (semantic, not type-based)

---

## Tests & Quality Assurance

**Unit Tests** (examples):

* `read_pdf` extracts text from a simple PDF.
* `read_pdf` respects `pages` ranges.
* `merge_pdf` produces a valid, readable output file.
* Error cases: missing file, invalid page ranges, wrong password.

**Tooling (suggested)**

```bash
pytest -q
ruff check .
black --check .
mypy .
```

---

## Packaging (optional)

### Define an entry point (example `pyproject.toml`)

```toml
[project]
name = "pdf-reader-cli"
version = "0.1.0"
description = "CLI to read and merge PDFs"
requires-python = ">=3.9"
dependencies = []  # your runtime dependencies

[project.scripts]
PDF_reader = "cli:ready"  # calls the ready() function from cli.py
```

> After installation, the tool can be invoked as `pdfreader`.

---

## Versioning & Releases

* SemVer recommended: `MAJOR.MINOR.PATCH`
* Tagged releases (Git tags), optionally attach build artifacts

---

## Contributing

Contributions are welcome! Please:

* Open issues with repro steps, expected/actual behavior, and system info
* Submit pull requests with tests and updated docs
* Follow code style & type hints

---

## Security

* Do not commit secrets to the repo or share them in issues (API keys, passwords)
* If you find a vulnerability, please report it privately: `raphael@hhaerle.de`

---

## License

 `LICENSE` MIT

---

## FAQ

**Why is there no text when reading a scanned PDF?**
The file likely contains only images. Without OCR, no text can be extracted.

**How do I specify multiple page ranges?**
Separate them with commas, e.g., `1-3,7,10-`.

**How is the merge order determined?**
The order is exactly the order of files after `-i/--input`.

**What happens if `--output` is missing?**
`core.merge_pdf` will likely fail with an error. Always provide `-o`.