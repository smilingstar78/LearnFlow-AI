from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_chat_chain(llm):

    prompt = PromptTemplate(

        template="""
You are a helpful AI assistant.

Use ONLY the provided context to answer the user's question.

Context:
{context}

User Question:
{query}

Instructions:
- Answer only using the provided context.
- If the user explicitly asks for another language (e.g. "answer in English", "translate to Urdu", "respond in French"), answer in that language.
- Otherwise, answer in the same language as the transcript.
- Do not mention that you translated unless the user asks.
- If the answer is not available in the context, politely say you don't know.
""",

        input_variables=["context", "query"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser