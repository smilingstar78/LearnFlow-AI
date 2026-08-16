from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_chat_chain(llm):

    prompt = PromptTemplate(

        template="""
You are a helpful AI assistant.

Previous Conversation:
{memory}

Video Context:
{context}

Current User Question:
{query}

Instructions:

- Use the previous conversation whenever it helps understand
  follow-up questions.
- Use the video context to answer questions about the video.
- If the user asks to translate, explain further, shorten,
  expand, or rewrite a previous answer, use the previous
  conversation.
- Otherwise answer using the video context.
- Do not invent information that is not present in the video
  context.
- If the answer cannot be found, politely say you don't know.
""",

        input_variables=[
            "memory",
            "context",
            "query"
        ]

    )

    parser = StrOutputParser()

    return prompt | llm | parser