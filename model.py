from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api._errors import NoTranscriptFound

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_chroma import Chroma

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

full_text = " ".join(snippet.text for snippet in transcript)

embeddings_model = HuggingFaceEmbeddings(model_name='BAAI/bge-small-en-v1.5')
chunks = SemanticChunker(embeddings_model)

docs = []

for snippet in transcript:

    docs.append(Document(page_content=snippet.text,
    metadata={
        "start":snippet.start,
        "duration":snippet.duration
    }))
text = chunks.split_documents(docs) #<--------------------------------------
print(f"Total chunks: {len(text)}")

chroma = Chroma(
            collection_name = 'transcripts',
            embedding_function = embeddings_model,
            persist_directory= "./chroma_db")

chroma.reset_collection()

chroma.add_documents(text)

retriever = chroma.as_retriever(search_kwargs={"k": 5})

parser = StrOutputParser()

prompt = PromptTemplate(
    template = """
    Use the given context to answer questions.
    Context:
    {doc_content}
    Question:
    {query}
    """,
    input_variables = ["doc_content", "query"]
)

summary_prompt = PromptTemplate(
    template = """
    Explain summary of the given context in easy words.

    Question:
    {query}
    Context:
    {full_text}

    """,
    input_variables = ['full_text']
)


llm = ChatGroq(api_key=os.getenv('GROQ_API_KEY'),
model='llama-3.3-70b-versatile')

chain = prompt | llm | parser

summary_chain = summary_prompt | llm | parser

while True:
    query = input('User: ')
    if 'summary' in query:
        result = summary_chain.invoke({'query':query, 'full_text':full_text})

    context = ""

    results = retriever.invoke(query)

    for doc in results:
        context+=f""""
        Timestamp: {doc.metadata['start']}

        content: 
        {doc.page_content}
        """

    # doc_content = "\n".join(doc.page_content for doc in results)
    result = chain.invoke({
        'query' : query,
        'doc_content':context
    })

    print('AI: ', result)
