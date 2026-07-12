from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api._errors import NoTranscriptFound

load_dotenv()

yt_api = YouTubeTranscriptApi()

def extract_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]

    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    return None

url = input("Paste URL: ")

try:
    transcript = yt_api.fetch(extract_video_id(url), languages=["en"])
    print("Using English transcript")

except NoTranscriptFound:
    transcript = yt_api.fetch(extract_video_id(url), languages=["hi"])
    print("Using Hindi transcript")

full_text = "".join(snippet.text for snippet in transcript)

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