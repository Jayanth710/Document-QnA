# app/loader.py

from PyPDF2 import PdfReader
from docx import Document as DocxDocument

def load_pdf(path):
    with open(path, "rb") as file:
        reader = PdfReader(file)
        return "".join(page.extract_text() for page in reader.pages)

def load_docx(path):
    doc = DocxDocument(path)
    return " ".join([para.text for para in doc.paragraphs if para.text.strip()])

def load_txt(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
