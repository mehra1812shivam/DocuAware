from docx import Document as DocxDocument

from app.services.extractors.base import BaseExtractor


class DocxExtractor(BaseExtractor):

    def extract_text(self, file_path: str) -> str:

        doc = DocxDocument(file_path)

        text_parts = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)

        return "\n".join(text_parts)