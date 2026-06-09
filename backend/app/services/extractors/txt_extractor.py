from app.services.extractors.base import BaseExtractor


class TxtExtractor(BaseExtractor):

    def extract_text(self, file_path: str) -> str:

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()