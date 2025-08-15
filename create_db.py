import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import shutil
from langchain_chroma import Chroma


### Set variables ###
DATA_PATH = "data_sources"

CHROMA_PATH = "chroma"

def get_embeddings():
    """Return an embeddings instance, preferring GPT4All with automatic fallback."""
    try:
        return GPT4AllEmbeddings(
            model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",
            gpt4all_kwargs={'allow_download': 'True'}
        )
    except Exception:
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vector_db():
    "Create vector DB from personal PDF files."
    documents = load_documents()
    doc_chunks = split_text(documents)
    save_to_chroma(doc_chunks)

def load_documents():
    "Load PDF documents from a folder using PyMuPDF for robust extraction."
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyMuPDFLoader)
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    "Split documents into chunks."
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_chroma(chunks: list[Document]):
    "Clear previous db, and save the new db."
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # create db
    db = Chroma.from_documents(
        chunks, get_embeddings(), persist_directory=CHROMA_PATH
    )
    
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    
if __name__ == "__main__":    
    create_vector_db()