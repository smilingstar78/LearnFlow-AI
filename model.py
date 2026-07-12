from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

yt_api = YouTubeTranscriptApi()

transcript = yt_api.fetch(input('Enter Video ID: '))

full_text = "".join(snippet.text for snippet in transcript)
# print(full_text)


parser = StrOutputParser()

prompt = PromptTemplate(
    template = """
    Use the given context to answer questions.
    Context:
    {full_text}
    Question:
    {query}
    """,
    input_variables = ["full_text", "query"]
)

llm = ChatGroq(api_key=os.getenv('GROQ_API_KEY'),
model='llama-3.3-70b-versatile')

chain = prompt | llm | parser
while True:
    query = input('User: ')
    result = chain.invoke({
        'query' : query,
        'full_text':full_text
    })

    print('AI: ', result)

# print(transcript)

# llm.invoke('What is your name?')