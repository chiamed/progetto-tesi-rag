import os
import fitz  # PyMuPDF
import docx
from typing import Union

from pydantic import BaseModel

class Parser(BaseModel):

    def extract_text_from_pdf(self, filepath: str) -> str:
        """To extract text from a PDF file"""
        text = ""
        try:
            with fitz.open(filepath) as pdf:
                for page in pdf:
                    text += page.get_text()
        except Exception as e:
            print(f"Error during PDF extraction: {e}")
        return text

    def extract_text_from_docx(self, filepath: str) -> str:
        """To extract text from a Word DOCX file"""
        text = ""
        try:
            doc = docx.Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error during DOCX extraction: {e}")
        return text

    def extract_text(self, filepath: str) -> Union[str, None]:
        """Wrapper to decide which extractor to use based on the extension"""
        if not os.path.isfile(filepath):
            print(f"File not found: {filepath}")
            return None

        if filepath.lower().endswith(".pdf"):
            return self.extract_text_from_pdf(filepath)

        elif filepath.lower().endswith(".docx"):
            return self.extract_text_from_docx(filepath)

        else:
            print(f"Unsupported file format: {filepath}")
            return None
