from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_study_notes_chain(llm):

    prompt = PromptTemplate(

        template="""
You are an expert study-notes creator.

You are given a section of a YouTube video transcript.

Transcript:
{transcript}

Create clear and useful study notes from this transcript.

Instructions:

- Identify the important concepts.
- Explain concepts in simple and easy language.
- Use headings and subheadings.
- Use bullet points.
- Include important definitions.
- Include important examples when present.
- Include important facts, steps, or processes.
- Do not add information that is not present in the transcript.
- Do not write unnecessary conversational text.
- Make the notes useful for exam revision.
- Keep the notes concise but informative.

Format the notes like:

## Topic

### Definition
- ...

### Important Points
- ...
- ...

### Example
- ...

### Key Takeaway
- ...

Only return the study notes.
""",

        input_variables=["transcript"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser