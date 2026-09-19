import os

import requests
from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv("BACKEND_URL")

if not BACKEND_URL:
    raise RuntimeError("BACKEND_URL is not configured")

BACKEND_URL = BACKEND_URL.rstrip("/")


def register(
    name: str,
    email: str,
    password: str,
    department: str,
):
    response = requests.post(
        f"{BACKEND_URL}/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "department": department,
        },
    )

    return response


def login(
    email: str,
    password: str,
):
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return response


def get_me(token: str):
    response = requests.get(
        f"{BACKEND_URL}/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    return response


def upload_document(
    token: str,
    file,
    confidentiality: str,
):
    response = requests.post(
        f"{BACKEND_URL}/documents/upload",
        headers={
            "Authorization": f"Bearer {token}",
        },
        files={
            "file": (
                file.name,
                file.getvalue(),
                file.type,
            )
        },
        data={
            "confidentiality": confidentiality,
        },
        timeout=120,
    )

    return response


def get_documents(token: str):
    response = requests.get(
        f"{BACKEND_URL}/documents",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    return response


def delete_document(
    token: str,
    document_id: str,
):
    response = requests.delete(
        f"{BACKEND_URL}/documents/{document_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    return response


def summarize_document(
    token: str,
    document_id: str,
):
    response = requests.post(
        f"{BACKEND_URL}/documents/{document_id}/summary",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=120,
    )

    return response


def chat(
    token: str,
    question: str,
    scope: str,
):
    response = requests.post(
        f"{BACKEND_URL}/chat",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "question": question,
            "scope": scope,
        },
        timeout=120,
    )

    return response