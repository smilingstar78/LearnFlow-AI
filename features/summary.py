from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_summary_chain(llm):

    prompt = PromptTemplate(

        template="""
Summarize the following transcript.

Transcript:
{full_text}

User Request:
{query}

Instructions:
- If the user asks for a specific language, write the summary in that language.
- Otherwise, summarize in the transcript's language.
- Keep the summary easy to understand.
""",

        input_variables=["full_text", "query"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser