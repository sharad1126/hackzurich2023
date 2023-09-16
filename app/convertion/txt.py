import os
import sys
from docx import Document
import fitz  # PyMuPDF
import extract_msg
from pathlib import Path
from shutil import copyfile
from extract_msg import Message


def remove_non_printable(text: str) -> str:
    return ''.join(char for char in text if char.isprintable())

def convert_docx_to_txt(input_file: str, output_dir: str):
    file_name = Path(input_file).stem
    doc = Document(input_file)
    output_path = Path(output_dir) / (file_name + ".txt")

    with open(output_path, "w", encoding="utf-8") as txt_file:
        for paragraph in doc.paragraphs:
            txt_file.write(remove_non_printable(paragraph.text) + " ")

    return output_path

def convert_pdf_to_txt(input_file: str, output_dir: str):
    file_name = Path(input_file).stem
    doc = fitz.open(input_file)
    output_path = Path(output_dir) / (file_name + ".txt")

    with open(output_path, "w", encoding="utf-8") as txt_file:
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            text = page.get_text()
            txt_file.write(text)

    return output_path
            
def convert_msg_to_txt(input_file: str, output_dir: str):
    attachments = Message(input_file).attachments

    if attachments:
        raise Exception(f"{input_file} has {len(attachments)} attachment(s)")

    try:
        msg = Message(input_file)

        # Construct the output file path
        base_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, os.path.splitext(base_name)[0] + ".txt")

        with open(output_file, "w") as txt_file:
            if msg.sender:
                txt_file.write(f"From: {msg.sender}\n")

            if msg.recipients:
                # Extract email addresses from recipient objects
                recipients_str = ', '.join([recipient.formatted for recipient in msg.recipients])
                txt_file.write(f"To: {recipients_str}\n")

            if msg.subject:
                txt_file.write(f"Subject: {msg.subject}\n")

            if msg.body:
                txt_file.write(f"{msg.body}\n")

        return output_file

    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        
def convert_other_to_txt(input_file: str, output_dir: str):
    file_name = Path(input_file).stem
    output_path = Path(output_dir) / (file_name + ".txt")
    copyfile(input_file, output_path)
    return output_path

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
    elif file_extension == ".msg":
        convert_msg_to_txt(input_file, output_dir)
    else:
        convert_other_to_txt(input_file, output_dir)

if __name__ == "__main__":
    main()