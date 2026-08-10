from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_quiz_chain(llm):

    prompt = PromptTemplate(

        template="""
You are an expert educational quiz creator.

You are given a section of a YouTube video transcript.

Transcript:
{transcript}

Create multiple-choice questions based ONLY on the information
contained in the transcript.

Instructions:

- Create 3 multiple-choice questions.
- Each question must have 4 options.
- Only ONE option should be correct.
- Make the questions test understanding, not just memorization.
- Do not use information that is not present in the transcript.
- Avoid duplicate questions.
- Include the correct answer after each question.
- Keep the explanations short and clear.

Use exactly this format:

Q1. Question?

A) Option
B) Option
C) Option
D) Option

Answer: B
Explanation: Short explanation.

Q2. Question?

A) Option
B) Option
C) Option
D) Option

Answer: A
Explanation: Short explanation.

Q3. Question?

A) Option
B) Option
C) Option
D) Option

Answer: D
Explanation: Short explanation.

Only return the quiz.
""",

        input_variables=["transcript"]

    )

    parser = StrOutputParser()

    return prompt | llm | parser