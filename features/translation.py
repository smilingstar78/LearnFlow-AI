from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_translation_chain(llm):

    prompt = PromptTemplate(

        template="""
You are a professional translator.

User Request:
{query}

Text to translate:
{text}

Instructions:
- Translate the given text according to the user's request.
- Do not answer the question.
- Do not summarize.
- Do not explain.
- Only return the translated text.
""",

        input_variables=["query", "text"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser