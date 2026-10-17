import PyPDF2
from PIL import Image

def extract_text_from_pdf(uploaded_file):
    """Extracts text content from an uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        extracted_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text
    except Exception as e:
        return f"Error reading PDF file: {e}"

def process_image(uploaded_file):
    """Processes an uploaded image file for AI vision."""
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        return f"Error reading Image file: {e}"