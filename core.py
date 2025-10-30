import os
from collections.abc import Sequence

from PyPDF2 import PdfMerger, PdfReader


def merge_pdf(output_path: str, input_paths: Sequence[str]) -> None:
    if not input_paths:
        raise ValueError("Input paths cannot be empty")

    abs_output_path = os.path.abspath(output_path)
    abs_input_path = [os.path.abspath(p) for p in input_paths]
    if abs_output_path in abs_input_path:
        raise ValueError("Output paths cannot be the same as input paths")

    missing = [p for p in input_paths if not os.path.isfile(p)]
    if missing:
        raise FileNotFoundError(f'File Not Found: {', '.join(missing)}')

    print("PFAD")
    print(abs_output_path)

    if len(abs_output_path) != 0:
        out_dir = os.path.dirname(abs_output_path)
        print(out_dir)
    else:
        out_dir = "./mergedFiles.pdf"
    merger = PdfMerger()

    try:
        for input_path in input_paths:
            merger.append(input_path)

        merger.write(abs_output_path)
        merger.close()
    except TypeError:
        raise f"Something went wrong"

def read_pdf(input_paths: str, selected_pages: list[int], password : str) -> str:
    if not input_paths:
        raise ValueError("Input paths cannot be empty")

    abs_input_path = os.path.abspath(input_paths)

    reader = PdfReader(abs_input_path)

    if reader.is_encrypted:
        if password:
            raise ValueError("PDF is encrypted. Password required!")
        if reader.decrypt(password) == 0:
            raise ValueError("Wrong PDF password!")

    pdf_pages = reader.pages

    if len(pdf_pages) == 0:
        raise ValueError("PDF is empty")

    pdf_parts = []
    if selected_pages is None:
        for page in pdf_pages:
            pdf_parts.append(page.extract_text() or "")
    else:
        total_pages = len(pdf_pages)
        bad = [ page for page in selected_pages if page < 0 or page >= total_pages ]
        if bad:
            raise ValueError(f'Invalide PDF pages: {bad} (o...{total_pages-1}')
        for i in selected_pages:
            pdf_parts.append(reader.pages[i].extract_text() or "")

    return "\n".join(pdf_parts)