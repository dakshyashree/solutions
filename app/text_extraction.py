import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a given PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {e}")
    return text