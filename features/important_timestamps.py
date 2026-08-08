from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_important_timestamps_chain(llm):

    prompt = PromptTemplate(

        template="""
You are analyzing a YouTube video transcript.

Your job is to identify the most important moments from the transcript.

Transcript:
{transcript}

Instructions:

- Identify important moments, concepts, explanations, examples, or topic changes.
- For every important moment, provide its timestamp.
- The timestamp is given in seconds in the transcript.
- Convert the timestamp into MM:SS format.
- Give a short description of what happens at that timestamp.
- Do not invent timestamps.
- Only use timestamps that appear in the provided transcript.
- Return 3 to 5 important moments from this section.

Format:

00:00 - Introduction to the topic
02:35 - Explanation of the main concept
07:42 - Important example
12:15 - Practical application

""",

        input_variables=["transcript"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser