import os
import fitz  # PyMuPDF
import docx
from typing import Union

from pydantic import BaseModel

class Parser(BaseModel):


    def extract_text_from_pdf(self, filepath: str) -> str:
        """Per estrarre testo da un file PDF"""
        text = ""
        try:
            with fitz.open(filepath) as pdf:
                for page in pdf:
                    text += page.get_text()
        except Exception as e:
            print(f"Errore durante l'estrazione del PDF: {e}")
        return text


    def extract_text_from_docx(self, filepath: str) -> str:
        """Per estrarre testo da un file Word DOCX"""
        text = ""
        try:
            doc = docx.Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Errore durante l'estrazione del DOCX: {e}")
        return text


    def extract_text(self, filepath: str) -> Union[str, None]:
        """Wrapper per decidere quale estrattore usare in base all'estensione"""
        if not os.path.isfile(filepath):
            print(f"File non trovato: {filepath}")
            return None

        if filepath.lower().endswith(".pdf"):
            return self.extract_text_from_pdf(filepath)

        elif filepath.lower().endswith(".docx"):
            return self.extract_text_from_docx(filepath)

        else:
            print(f"Formato file non supportato: {filepath}")
            return None
