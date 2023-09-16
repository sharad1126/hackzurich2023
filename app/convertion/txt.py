import os
import sys
from docx import Document
import fitz  # PyMuPDF
import extract_msg
from pathlib import Path
from shutil import copyfile


def remove_non_printable(text: str) -> str:
    return ''.join(char for char in text if char.isprintable())

def convert_docx_to_txt(input_file: str, output_dir: str):
    file_name = Path(input_file).stem
    doc = Document(input_file)
    output_path = Path(output_dir) / (file_name + ".txt")

    with open(output_path, "w", encoding="utf-8") as txt_file:
        for paragraph in doc.paragraphs:
            txt_file.write(remove_non_printable(paragraph.text) + "\n")

def convert_pdf_to_txt(input_file: str, output_dir: str):
    file_name = Path(input_file).stem
    doc = fitz.open(input_file)
    output_path = Path(output_dir) / (file_name + ".txt")

    with open(output_path, "w", encoding="utf-8") as txt_file:
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            text = page.get_text("block")
            txt_file.write(text)
            
def convert_msg_to_txt(input_file: str, output_dir: str):
    pass

def convert_other_to_txt(input_file: str, output_dir: str):
    file_name = Path(input_file).stem
    output_path = Path(output_dir) / (file_name + ".txt")
    copyfile(input_file, output_path)

def main():
    if len(sys.argv) != 3:
        print("Usage: python txt.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    file_extension = Path(input_file).suffix.lower()

    if file_extension == ".docx":
        convert_docx_to_txt(input_file, output_dir)
    elif file_extension == ".pdf":
        convert_pdf_to_txt(input_file, output_dir)
    else:
        convert_other_to_txt(input_file, output_dir)

if __name__ == "__main__":
    main()