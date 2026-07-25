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
        You are answering a question about a specific moment
        in a YouTube video.

        The user wants to know what was being said or discussed
        at the requested timestamp.

        Transcript spoken around that timestamp:

        {context}

        User question:

        {query}

        Answer directly and naturally.

        Do not explain how timestamps are converted into seconds.
        Do not discuss ambiguity about the timestamp.
        Do not mention missing units.

        Simply explain what was being said or discussed at that
        moment based on the transcript provided.

        If the transcript context is incomplete, say what can be
        understood from the available transcript.
        """,

        input_variables=[
            "context",
            "query"
        ]
    )

    parser = StrOutputParser()

    return prompt | llm | parser