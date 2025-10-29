import os
from collections.abc import Sequence

from PyPDF2 import PdfMerger



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