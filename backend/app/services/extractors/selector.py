from app.core.enums import FileType

from app.services.extractors.pdf_extractor import PdfExtractor
from app.services.extractors.docx_extractor import DocxExtractor
from app.services.extractors.txt_extractor import TxtExtractor


class TextExtractorSelector:

    def __init__(self):
        self.pdf = PdfExtractor()
        self.docx = DocxExtractor()
        self.txt = TxtExtractor()

    def extract(self, file_type: FileType, file_path: str) -> str:

        if file_type == FileType.PDF:
            return self.pdf.extract_text(file_path)

        if file_type == FileType.DOCX:
            return self.docx.extract_text(file_path)

        if file_type == FileType.TXT:
            return self.txt.extract_text(file_path)

        raise ValueError(f"Unsupported file type: {file_type}")