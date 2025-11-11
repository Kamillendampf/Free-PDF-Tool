import os
from collections.abc import Sequence
from PyPDF2 import PdfMerger, PdfReader
from pdf2docx import Converter


import helper

def merge_pdf(output_path: str, input_paths: Sequence[str]) -> None:

    print("von merge_pdf" +output_path)
    if not input_paths:
        raise ValueError("Input paths cannot be empty")

    abs_output_path : str = os.path.abspath(output_path)
    abs_input_path : list[str] = [os.path.abspath(p) for p in input_paths]
    if abs_output_path in abs_input_path:
        raise ValueError("Output paths cannot be the same as input paths")

    missing : list[str] = [p for p in input_paths if not os.path.isfile(p)]
    if missing:
        raise FileNotFoundError('File Not Found:' + ', '.join(missing))

    merger : PdfMerger = PdfMerger()

    try:
        for input_path in input_paths:
            merger.append(input_path)

        merger.write(abs_output_path)
        merger.close()
    except TypeError:
        raise f"Something went wrong"

def read_pdf(input_paths: str, raw_selected_pages: str, password : str) -> str:
    if raw_selected_pages:
        selected_pages : list[tuple[int]] = helper.cmd_str_pages_2_int_tuple(raw_selected_pages)
    else:
        selected_pages = None

    if not input_paths:
        raise ValueError("Input paths cannot be empty")

    abs_input_path : str = os.path.abspath(input_paths)

    reader : PdfReader = PdfReader(abs_input_path)

    helper.decrypt_pdf(reader, password)

    pdf_pages : reader.pages = reader.pages

    if len(pdf_pages) == 0:
        raise ValueError("PDF is empty")

    pdf_parts = []
    if selected_pages is None:
        for page in pdf_pages:
            pdf_parts.append(page.extract_text() or "")
    else:
        total_pages = len(pdf_pages)

        bad = [ page for page in selected_pages if (page[0] < 0 or page[0] >= total_pages) or (page[1] < 0 or page[1] >= total_pages) ]
        if bad:
            raise ValueError(f'Invalide PDF pages: {bad} (o...{total_pages-1}')
        for start_end in selected_pages:
            for i in range(start_end[0], start_end[1]+1):
                pdf_parts.append(reader.pages[i].extract_text() or "")

    return "\n".join(pdf_parts)

def convert_pdf_to_docx(input_paths : str, output_path_docx : str, raw_selected_pages : str, password : str):

    convert = Converter(input_paths)

    if raw_selected_pages:
        print(f"[INFO] Converting PDF pages {raw_selected_pages} to docx")
        to_include_pages : list[tuple[int]] = helper.cmd_str_pages_2_int_tuple(raw_selected_pages)
        print("to_include pages "+ str(to_include_pages[0][0]))
        for i in range(len(to_include_pages)):
            convert.convert(output_path_docx, to_include_pages[i][0][0], to_include_pages[i][1][0]+1)
    else:
        print("[INFO] Converting all PDF pages to docx")
        convert.convert(output_path_docx)

    convert.close()