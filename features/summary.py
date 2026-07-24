from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_summary_chain(llm):

    summary_prompt = PromptTemplate(

        template="""
        Give a summary of the following video transcript
        in simple and easy-to-understand words.

        Transcript:
        {full_text}
        """,

        input_variables=[
            "full_text"
        ]
    )

    parser = StrOutputParser()

    summary_chain = summary_prompt | llm | parser

    return summary_chain