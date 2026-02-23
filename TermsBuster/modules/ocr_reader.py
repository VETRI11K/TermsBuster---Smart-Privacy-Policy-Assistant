# ocr_reader.py
import pdfplumber
from PIL import Image
import pytesseract

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_image(pil_image):
    return pytesseract.image_to_string(pil_image)
