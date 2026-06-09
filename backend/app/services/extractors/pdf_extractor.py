import pdfplumber

from app.services.extractors.base import BaseExtractor


class PdfExtractor(BaseExtractor):

    def extract_text(self, file_path: str) -> str:

        text_parts = []

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    text_parts.append(text)

        return "\n".join(text_parts)