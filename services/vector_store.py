from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_chroma import Chroma


def create_vector_store(transcript):

    embeddings_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    chunks = SemanticChunker(embeddings_model)

    docs = []

    for snippet in transcript:

        docs.append(
            Document(
                page_content=snippet.text,

                metadata={
                    "start": snippet.start,
                    "duration": snippet.duration
                }
            )
        )

    text = chunks.split_documents(docs)

    print(f"Total chunks: {len(text)}")

    chroma = Chroma(
        collection_name="transcripts",

        embedding_function=embeddings_model,

        persist_directory="./chroma_db"
    )

    chroma.reset_collection()

    chroma.add_documents(text)

    retriever = chroma.as_retriever(
        search_kwargs={"k": 5}
    )

    return retriever