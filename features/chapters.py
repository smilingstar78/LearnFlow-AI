from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_chapters_chain(llm):

    prompt = PromptTemplate(

        template="""
You are an expert at organizing educational video transcripts.

You are given a section of a YouTube video transcript with timestamps.

Transcript:
{transcript}

Identify the major topics discussed in this section and create
clear video chapters.

Instructions:

- Identify meaningful topic changes.
- Do not create a chapter for every small point.
- Each chapter should represent a substantial topic or section.
- Use the timestamp where that topic begins.
- The timestamp is provided in seconds.
- Convert seconds into MM:SS format.
- Do not invent timestamps.
- Use only timestamps that appear in the transcript.
- Give each chapter a short, descriptive title.
- Return 2 to 5 chapters for this section.

Use exactly this format:

00:00 - Introduction
03:25 - What is FastAPI?
08:09 - Pydantic and Data Validation

Only return the chapters.
""",

        input_variables=["transcript"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser