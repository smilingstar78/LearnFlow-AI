from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_overview_chain(llm):
    overview_prompt = PromptTemplate(
        template="""
        Analyze the following YouTube transcript.

        Identify:
        1. What is the main topic of the video?
        2. What are the main concepts discussed?
        3. What is the purpose of the video?
        4. What should someone learn after watching it?

        Transcript:
        {full_text}
        """,

        input_variables=["full_text"]
    )

    parser = StrOutputParser()
    overview_chain = overview_prompt | llm | parser

    return overview_chain