from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re


def extract_timestamp(query):

    match = re.search(r'(\d{1,2}):(\d{2})', query)

    if not match:
        return None

    minutes = int(match.group(1))
    seconds = int(match.group(2))

    return minutes * 60 + seconds


def get_timestamp_context(transcript, target_seconds):

    context = []

    window_before = 10
    window_after = 10

    for snippet in transcript:

        start = snippet.start

        end = snippet.start + snippet.duration

        if (
            end >= target_seconds - window_before
            and start <= target_seconds + window_after
        ):

            context.append(
                f"[{start:.2f}s] {snippet.text}"
            )

    return " ".join(context)


def create_timestamp_chain(llm):

    prompt = PromptTemplate(

    template="""
The user asked about a specific moment in the video.

Transcript around that timestamp:

{context}

User Request:
{query}

Instructions:
- Explain what was being discussed around this timestamp.
- If the user requests another language, answer in that language.
- Otherwise, answer in the transcript's language.
- Never explain timestamp conversion.
""",

    input_variables=["context", "query"]

)

    parser = StrOutputParser()

    return prompt | llm | parser