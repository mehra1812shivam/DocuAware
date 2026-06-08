from app.core.enums import FileType


def get_file_type(filename: str) -> FileType:

    extension = filename.split(".")[-1].lower()

    if extension == "pdf":
        return FileType.PDF

    if extension == "docx":
        return FileType.DOCX

    if extension == "txt":
        return FileType.TXT

    raise ValueError("Unsupported file type")