from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_flashcards_chain(llm):

    prompt = PromptTemplate(

        template="""
You are an expert study assistant.

You are given a section of a YouTube video transcript.

Transcript:
{transcript}

Create useful study flashcards based ONLY on the information
contained in the transcript.

Instructions:

- Create 3 flashcards.
- Focus on important concepts, definitions, facts, and explanations.
- Questions should test understanding.
- Answers should be short but complete.
- Do not add information that is not present in the transcript.
- Do not create duplicate flashcards.

Use exactly this format:

Flashcard 1

Question:
What is ...?

Answer:
...


Flashcard 2

Question:
Why ...?

Answer:
...


Flashcard 3

Question:
What is the purpose of ...?

Answer:
...

Only return the flashcards.
""",

        input_variables=["transcript"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser