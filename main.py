from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


from utils.url import extract_video_id

from services.transcript_service import fetch_transcript

from services.vector_store import create_vector_store

from features.chat import create_chat_chain

from features.summary import create_summary_chain


load_dotenv()


# -----------------------------------
# 1. Get YouTube URL
# -----------------------------------

url = input("Paste URL: ")


# -----------------------------------
# 2. Extract Video ID
# -----------------------------------

video_id = extract_video_id(url)


# -----------------------------------
# 3. Fetch Transcript
# -----------------------------------

transcript = fetch_transcript(video_id)


# -----------------------------------
# 4. Create Full Text
# -----------------------------------

full_text = " ".join(
    snippet.text
    for snippet in transcript
)


# -----------------------------------
# 5. Create Vector Store
# -----------------------------------

retriever = create_vector_store(transcript)


# -----------------------------------
# 6. Create LLM
# -----------------------------------

llm = ChatGroq(

    api_key=os.getenv("GROQ_API_KEY"),

    model="llama-3.3-70b-versatile"
)


# -----------------------------------
# 7. Create Chains
# -----------------------------------

chat_chain = create_chat_chain(llm)

summary_chain = create_summary_chain(llm)


# -----------------------------------
# 8. Chat Loop
# -----------------------------------

while True:

    query = input("\nUser: ")


    # -------------------------------
    # Summary Feature
    # -------------------------------

    if "summary" in query.lower():

        result = summary_chain.invoke({

            "full_text": full_text

        })

        print("\nAI:", result)

        continue


    # -------------------------------
    # Normal RAG Chat
    # -------------------------------

    results = retriever.invoke(query)


    context = ""

    for doc in results:

        context += f"""

        Timestamp: {doc.metadata['start']}

        Content:
        {doc.page_content}

        """


    result = chat_chain.invoke({

        "query": query,

        "context": context

    })


    print("\nAI:", result)