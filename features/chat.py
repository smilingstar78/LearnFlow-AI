from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_chat_chain(llm):

    prompt = PromptTemplate(

        template="""
        You are a helpful AI assistant that can answer questions
        about a YouTube video.

        You have access to video context, but you do NOT need to use
        it for every message.

        Rules:

        1. If the user asks a question related to the video,
        use the provided context to answer.

        2. If the user is having normal conversation, such as saying
        hello, thank you, or asking how you are, respond naturally.

        3. If the answer is not available in the video context,
        honestly say that the video does not provide enough information.

        Context:
        {context}

        User:
        {query}
        """,

        input_variables=[
            "context",
            "query"
        ]
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    return chain