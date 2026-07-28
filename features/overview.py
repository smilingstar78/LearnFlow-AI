from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_overview_chain(llm):

    prompt = PromptTemplate(

        template="""
Read the transcript and explain what this video is about.

Transcript:
{full_text}

User Request:
{query}

Instructions:
- If the user requests another language, answer in that language.
- Otherwise, answer in the transcript's language.
- Explain the main topic and key ideas.
""",

        input_variables=["full_text", "query"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser