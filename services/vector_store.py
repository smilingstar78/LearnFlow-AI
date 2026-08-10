from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_chroma import Chroma


def create_vector_store(video_transcripts):

    embeddings_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    chunks = SemanticChunker(embeddings_model)

    documents = []

    # -----------------------------------
    # Create documents from all videos
    # -----------------------------------

    for video in video_transcripts:

        video_id = video["video_id"]
        transcript = video["transcript"]

        docs = []

        for snippet in transcript:

            docs.append(

                Document(

                    page_content=snippet.text,

                    metadata={

                        "video_id": video_id,

                        "start": snippet.start,

                        "duration": snippet.duration

                    }

                )

            )


        video_chunks = chunks.split_documents(docs)

        documents.extend(video_chunks)


    print(
        f"Total chunks from all videos: "
        f"{len(documents)}"
    )


    # -----------------------------------
    # Create Chroma
    # -----------------------------------

    chroma = Chroma(

        collection_name="transcripts",

        embedding_function=embeddings_model,

        persist_directory="./chroma_db"

    )


    chroma.reset_collection()


    chroma.add_documents(documents)


    return chroma.as_retriever(

        search_kwargs={"k": 5}

    )