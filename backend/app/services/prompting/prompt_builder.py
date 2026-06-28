from langchain_core.prompts import ChatPromptTemplate

class PromptBuilder:
    def __init__(self):

        self.prompt = ChatPromptTemplate.from_template(
            """You are DocuAware.

You answer ONLY using the supplied document context.

Rules:

- Never fabricate information.
- If the provided context does not contain enough information to answer the question, reply exactly:

"I couldn't find this information in the selected documents."

Do not use outside knowledge.

Context:
--------
{context}

Question:
---------
{question}

Answer:
"""
        )

    def build(
        self,
        question: str,
        chunks: list
    ) -> str:
        context = "\n\n".join(
            chunk.payload["content"]
            for chunk in chunks
        )

        return self.prompt.format(
            context=context,
            question=question
        )
        