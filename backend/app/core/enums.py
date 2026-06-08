from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class Department(str, Enum):
    ENGINEERING = "ENGINEERING"
    HR = "HR"
    FINANCE = "FINANCE"
    LEGAL = "LEGAL"
    OPERATIONS = "OPERATIONS"

class DocumentStatus(str, Enum):
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"

class FileType(str, Enum):
    PDF = "PDF"
    DOCX = "DOCX"
    TXT = "TXT"