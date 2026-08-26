from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_translation_chain(llm):

    prompt = PromptTemplate(

        template="""
You are a professional translator.

Translation request:
{query}

Text to translate:
{text}

Instructions:
- Follow the translation request exactly.
- Translate the ENTIRE text.
- Preserve the original meaning and tone.
- Preserve timestamps exactly.
- Preserve numbers exactly.
- Preserve names exactly.
- Preserve technical terms when appropriate.
- Preserve the original formatting as much as possible.
- Do NOT summarize.
- Do NOT explain.
- Do NOT answer the user's request.
- Do NOT add any information.
- Return ONLY the translated text.
""",

        input_variables=[
            "query",
            "text"
        ]

    )

    parser = StrOutputParser()

    return prompt | llm | parser