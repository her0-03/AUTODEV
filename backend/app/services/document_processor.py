import PyPDF2
import docx
import openpyxl
import pandas as pd
from PIL import Image
import pytesseract
import markdown
from pathlib import Path

class DocumentProcessor:
    @staticmethod
    def process_file(file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return DocumentProcessor._process_pdf(file_path)
        elif ext in ['.doc', '.docx']:
            return DocumentProcessor._process_docx(file_path)
        elif ext in ['.xls', '.xlsx']:
            return DocumentProcessor._process_excel(file_path)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return DocumentProcessor._process_image(file_path)
        elif ext == '.md':
            return DocumentProcessor._process_markdown(file_path)
        elif ext == '.txt':
            return DocumentProcessor._process_text(file_path)
        else:
            return ""
    
    @staticmethod
    def _process_pdf(file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def _process_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    @staticmethod
    def _process_excel(file_path: str) -> str:
        df = pd.read_excel(file_path)
        return df.to_string()
    
    @staticmethod
    def _process_image(file_path: str) -> str:
        try:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img)
        except:
            return ""
    
    @staticmethod
    def _process_markdown(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def _process_text(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
