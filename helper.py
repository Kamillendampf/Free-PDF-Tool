from PyPDF2 import PdfReader
from select import select


def cmd_str_pages_2_int_tuple(raw_selected_pages : str) -> list[tuple[int]]:
    selected_pages : list = []
    raw_selected_pages_list : list[str] = raw_selected_pages.split(',')
    for page in raw_selected_pages_list:
        if "-" in page:
            start_end_of_to_read_pages =  convert_str_pages_2_int_pages(page.split("-"))
            selected_pages.append((start_end_of_to_read_pages[0], start_end_of_to_read_pages[1]))
        else:
            selected_pages.append((convert_str_pages_2_int_pages([page]), convert_str_pages_2_int_pages([page])))

def convert_str_pages_2_int_pages(raw_selected_pages : list[str]) -> list[int]:
    try:
        selected_pages : list[int] = [int(selected_page) for selected_page in raw_selected_pages ]
    except ValueError:
        raise ValueError("Selected pages must be a positive numbers")

    return selected_pages

def decrypt_pdf(reader : PdfReader, password : str):
    if reader.is_encrypted:
        if password:
            raise ValueError("PDF is encrypted. Password required!")
        if reader.decrypt(password) == 0:
            raise ValueError("Wrong PDF password!")