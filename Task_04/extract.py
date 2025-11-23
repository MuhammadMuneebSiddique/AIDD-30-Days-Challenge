from typing import Annotated
import pypdf
import re
from agents import function_tool

@function_tool
def extract_text_from_pdf(file_path: Annotated[str, "The path to the PDF file to extract text from."]) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        return f"Error extracting text from PDF: {e}"
    return text

@function_tool
def clean_text(text: Annotated[str, "The raw text extracted from a PDF to clean."]) -> str:
    """Removes newlines and extra spaces from the given text."""
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
