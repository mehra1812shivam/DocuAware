
import requests
import streamlit as st
from streamlit_cookies_controller import CookieController

from api import (
    chat,
    delete_document,
    get_documents,
    get_me,
    login,
    register,
    summarize_document,
    upload_document,
)


st.set_page_config(
    page_title="DocuAware",
    page_icon="📄",
    layout="centered",
)


# ---------------------------------------------------------
# Cookie controller
# ---------------------------------------------------------

if "cookie_controller" not in st.session_state:
    st.session_state.cookie_controller = CookieController()

cookies = st.session_state.cookie_controller


# ---------------------------------------------------------
# Session initialization
# ---------------------------------------------------------

def initialize_session():
    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = None

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    if "summaries" not in st.session_state:
        st.session_state.summaries = {}

    if "auth_initialized" not in st.session_state:
        st.session_state.auth_initialized = False

    if "cookie_checked" not in st.session_state:
        st.session_state.cookie_checked = False

    # Temporary chatbot history.
    # This is stored only in the current Streamlit session.
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

def restore_authentication():
    if st.session_state.auth_initialized:
        return

    saved_token = cookies.get("docuaware_token")

    if saved_token is None and not st.session_state.cookie_checked:
        st.session_state.cookie_checked = True
        st.rerun()

    if saved_token:
        try:
            response = get_me(saved_token)

            if response.status_code == 200:
                st.session_state.token = saved_token
                st.session_state.user = response.json()

            else:
                cookies.remove("docuaware_token")

        except requests.RequestException:
            pass

    st.session_state.auth_initialized = True


def logout():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.auth_mode = "login"
    st.session_state.summaries = {}
    st.session_state.chat_messages = []
    st.session_state.auth_initialized = True
    st.session_state.cookie_checked = True

    cookies.remove("docuaware_token")

    st.rerun()


# ---------------------------------------------------------
# Branding
# ---------------------------------------------------------

def show_branding():
    st.markdown(
        """
        <style>
        .brand {
            text-align: center;
            margin-top: 45px;
            margin-bottom: 28px;
        }

        .brand-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .brand-subtitle {
            font-size: 16px;
            color: #6b7280;
        }
        </style>

        <div class="brand">
            <div class="brand-title">📄 DocuAware</div>
            <div class="brand-subtitle">
                AI-powered document intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------

def show_login():
    st.subheader("Welcome back")
    st.caption("Sign in to continue to your documents.")

    with st.form("login_form"):
        email = st.text_input(
            "Email",
            placeholder="you@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        submitted = st.form_submit_button(
            "Sign in",
            use_container_width=True,
        )

    if submitted:
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        try:
            response = login(
                email=email.strip(),
                password=password,
            )

            if response.status_code == 200:
                data = response.json()
                token = data["access_token"]

                me_response = get_me(token)

                if me_response.status_code == 200:
                    st.session_state.token = token
                    st.session_state.user = me_response.json()
                    st.session_state.auth_initialized = True
                    st.session_state.cookie_checked = True

                    cookies.set(
                        "docuaware_token",
                        token,
                        max_age=60 * 60 * 24 * 7,
                    )

                    st.rerun()

                else:
                    st.error(
                        "Login succeeded, but user information "
                        "could not be loaded."
                    )

            else:
                try:
                    detail = response.json().get(
                        "detail",
                        "Login failed.",
                    )
                except ValueError:
                    detail = "Login failed."

                st.error(detail)

        except requests.RequestException:
            st.error(
                "Unable to connect to the backend. "
                "Please make sure FastAPI is running."
            )

    st.divider()

    st.write("Don't have an account?")

    if st.button(
        "Create an account",
        use_container_width=True,
    ):
        st.session_state.auth_mode = "register"
        st.rerun()


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------

def show_register():
    st.subheader("Create your account")
    st.caption("Register to start using DocuAware.")

    with st.form("register_form"):
        name = st.text_input(
            "Full name",
            placeholder="Your name",
        )

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
        )

        department = st.selectbox(
            "Department",
            options=[
                "ENGINEERING",
                "HR",
                "FINANCE",
                "LEGAL",
                "OPERATIONS",
                "OTHER",
            ],
        )

        submitted = st.form_submit_button(
            "Create account",
            use_container_width=True,
        )

    if submitted:
        if not name or not email or not password:
            st.error("Please fill in all required fields.")
            return

        try:
            response = register(
                name=name.strip(),
                email=email.strip(),
                password=password,
                department=department,
            )

            if response.status_code in (200, 201):
                st.success(
                    "Account created successfully. "
                    "You can now sign in."
                )

                st.session_state.auth_mode = "login"
                st.rerun()

            else:
                try:
                    detail = response.json().get(
                        "detail",
                        "Registration failed.",
                    )
                except ValueError:
                    detail = "Registration failed."

                st.error(detail)

        except requests.RequestException:
            st.error(
                "Unable to connect to the backend. "
                "Please make sure FastAPI is running."
            )

    st.divider()

    st.write("Already have an account?")

    if st.button(
        "Back to sign in",
        use_container_width=True,
    ):
        st.session_state.auth_mode = "login"
        st.rerun()


# ---------------------------------------------------------
# Authentication screen
# ---------------------------------------------------------

def show_auth():
    show_branding()

    with st.container(border=True):
        if st.session_state.auth_mode == "login":
            show_login()
        else:
            show_register()


# ---------------------------------------------------------
# Documents
# ---------------------------------------------------------

def load_documents():
    try:
        response = get_documents(st.session_state.token)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            st.error(
                "Your session has expired. Please log in again."
            )
            logout()

        st.error("Unable to load documents.")
        return []

    except requests.RequestException:
        st.error(
            "Unable to connect to the backend. "
            "Please make sure FastAPI is running."
        )
        return []


# ---------------------------------------------------------
# Upload
# ---------------------------------------------------------

def show_upload():
    st.subheader("Upload document")
    st.caption(
        "Supported formats: PDF, DOCX, and TXT."
    )

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "docx", "txt"],
    )

    confidentiality = st.selectbox(
        "Confidentiality",
        options=[
            "PUBLIC",
            "INTERNAL",
            "CONFIDENTIAL",
        ],
    )

    if st.button(
        "Upload document",
        type="primary",
        use_container_width=True,
    ):
        if uploaded_file is None:
            st.warning("Please select a document first.")
            return

        try:
            with st.spinner(
                "Uploading and processing document..."
            ):
                response = upload_document(
                    token=st.session_state.token,
                    file=uploaded_file,
                    confidentiality=confidentiality,
                )

            if response.status_code in (200, 201):
                st.success(
                    f"'{uploaded_file.name}' uploaded successfully."
                )
                st.rerun()

            else:
                try:
                    detail = response.json().get(
                        "detail",
                        "Document upload failed.",
                    )
                except ValueError:
                    detail = "Document upload failed."

                st.error(detail)

        except requests.RequestException:
            st.error(
                "Unable to connect to the backend."
            )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

def show_summary(document_id: str):
    if document_id in st.session_state.summaries:
        st.markdown("**Summary**")
        st.write(
            st.session_state.summaries[document_id]
        )


def generate_summary(document_id: str):
    try:
        with st.spinner("Generating summary..."):
            response = summarize_document(
                token=st.session_state.token,
                document_id=document_id,
            )

        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary")

            if summary:
                st.session_state.summaries[document_id] = summary
                st.rerun()

            st.error(
                "Summary was generated, but no summary "
                "text was returned."
            )

        elif response.status_code == 403:
            st.error(
                "You do not have permission to summarize this document."
            )

        elif response.status_code == 404:
            st.error("Document not found.")

        else:
            try:
                detail = response.json().get(
                    "detail",
                    "Failed to generate summary.",
                )
            except ValueError:
                detail = "Failed to generate summary."

            st.error(detail)

    except requests.RequestException:
        st.error(
            "Unable to connect to the backend."
        )


# ---------------------------------------------------------
# RAG Chat
# ---------------------------------------------------------

def show_chat():
    st.subheader("Ask your documents")

    st.caption(
        "Ask questions and get answers based only on "
        "documents you are authorized to access."
    )

    scope = st.selectbox(
        "Search scope",
        options=[
            "MY_DOCUMENTS",
            "ALL_ACCESSIBLE",
        ],
        format_func=lambda value: (
            "My documents"
            if value == "MY_DOCUMENTS"
            else "All accessible documents"
        ),
        key="chat_scope",
    )

    # Display temporary conversation history.
    # This is NOT sent to the backend and is NOT persisted.
    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        filename = source.get(
                            "filename",
                            "Unknown document",
                        )

                        chunk_index = source.get(
                            "chunk_index",
                            "-",
                        )

                        st.caption(
                            f"📄 {filename} · "
                            f"Chunk {chunk_index}"
                        )

    question = st.chat_input(
        "Ask something about your documents..."
    )

    if question:
        question = question.strip()

        if not question:
            return

        # Store user's message only in current session.
        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        try:
            with st.chat_message("assistant"):

                with st.spinner(
                    "Searching your documents..."
                ):
                    response = chat(
                        token=st.session_state.token,
                        question=question,
                        scope=scope,
                    )

                if response.status_code == 200:
                    data = response.json()

                    answer = data.get("answer")
                    sources = data.get("sources", [])

                    if answer:
                        st.markdown(answer)
                    else:
                        answer = (
                            "No relevant information was found "
                            "in the accessible documents."
                        )
                        st.info(answer)

                    if sources:
                        with st.expander("Sources"):
                            for source in sources:
                                filename = source.get(
                                    "filename",
                                    "Unknown document",
                                )

                                chunk_index = source.get(
                                    "chunk_index",
                                    "-",
                                )

                                st.caption(
                                    f"📄 {filename} · "
                                    f"Chunk {chunk_index}"
                                )

                    # Store assistant response only in
                    # current Streamlit session.
                    st.session_state.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )

                elif response.status_code == 401:
                    st.error(
                        "Your session has expired. "
                        "Please log in again."
                    )
                    logout()

                elif response.status_code == 403:
                    st.error(
                        "You do not have permission to access "
                        "these documents."
                    )

                else:
                    try:
                        detail = response.json().get(
                            "detail",
                            "Unable to process your question.",
                        )
                    except ValueError:
                        detail = (
                            "Unable to process your question."
                        )

                    st.error(detail)

        except requests.RequestException:
            st.error(
                "Unable to connect to the backend. "
                "Please make sure FastAPI is running."
            )

    if st.session_state.chat_messages:
        if st.button(
            "Clear conversation",
            use_container_width=True,
            key="clear_chat",
        ):
            st.session_state.chat_messages = []
            st.rerun()


# ---------------------------------------------------------
# Document list
# ---------------------------------------------------------

def show_documents():
    st.subheader("Your documents")

    documents = load_documents()

    if not documents:
        st.info(
            "No documents available yet. "
            "Upload your first document above."
        )
        return

    for document in documents:
        document_id = document.get("id")

        filename = document.get(
            "filename",
            "Unnamed document",
        )

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(
                    f"**📄 {filename}**"
                )

                st.caption(
                    f"Type: {document.get('file_type', '-')}"
                )

                st.caption(
                    f"Department: "
                    f"{document.get('department', '-')}"
                )

                st.caption(
                    f"Confidentiality: "
                    f"{document.get('confidentiality', '-')}"
                )

                status = document.get(
                    "status",
                    "-",
                )

                if status == "READY":
                    st.success(
                        "READY",
                        icon="✅",
                    )

                elif status == "PROCESSING":
                    st.info(
                        "PROCESSING",
                        icon="⏳",
                    )

                elif status == "FAILED":
                    st.error(
                        "FAILED",
                        icon="❌",
                    )

                else:
                    st.caption(
                        f"Status: {status}"
                    )

            with col2:
                if st.button(
                    "Summarize",
                    key=f"summary_{document_id}",
                    use_container_width=True,
                ):
                    generate_summary(document_id)

                if st.button(
                    "Delete",
                    key=f"delete_{document_id}",
                    use_container_width=True,
                ):
                    try:
                        response = delete_document(
                            token=st.session_state.token,
                            document_id=document_id,
                        )

                        if response.status_code == 204:
                            st.session_state.summaries.pop(
                                document_id,
                                None,
                            )

                            st.success("Deleted.")
                            st.rerun()

                        else:
                            try:
                                detail = response.json().get(
                                    "detail",
                                    "Delete failed.",
                                )
                            except ValueError:
                                detail = "Delete failed."

                            st.error(detail)

                    except requests.RequestException:
                        st.error(
                            "Unable to connect to the backend."
                        )

            show_summary(document_id)


# ---------------------------------------------------------
# Main application
# ---------------------------------------------------------

def show_application():
    user = st.session_state.user

    st.sidebar.title("📄 DocuAware")
    st.sidebar.caption(
        "AI-powered document intelligence"
    )

    st.sidebar.divider()

    if user:
        st.sidebar.subheader("Account")

        st.sidebar.write(
            f"**{user.get('name', 'User')}**"
        )

        st.sidebar.caption(
            user.get("email", "")
        )

        st.sidebar.caption(
            f"Department: "
            f"{user.get('department', '-')}"
        )

        st.sidebar.caption(
            f"Role: {user.get('role', '-')}"
        )

    st.sidebar.divider()

    if st.sidebar.button(
        "Logout",
        use_container_width=True,
    ):
        logout()

    st.title("DocuAware")

    if user:
        st.write(
            f"Hello, **{user.get('name', 'there')}** 👋"
        )

    st.caption(
        "Manage documents, generate summaries, "
        "and ask questions using AI."
    )

    st.divider()

    show_upload()

    st.divider()

    show_documents()

    st.divider()

    show_chat()


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

def main():
    initialize_session()
    restore_authentication()

    if st.session_state.token:
        show_application()
    else:
        show_auth()


if __name__ == "__main__":
    main()

