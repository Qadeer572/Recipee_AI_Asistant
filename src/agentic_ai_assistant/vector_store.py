import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Configuration
VECTOR_STORE_PATH = "vectorstore/recipe_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def create_embeddings():
    """
    Create embedding model
    """
    print("🔧 Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✅ Embedding model loaded!")
    return embeddings


def create_vector_store(pdf_path, embeddings):
    """
    Create vector store from PDF
    """
    print(f"\n📄 Loading PDF: {pdf_path}")
    
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} pages")
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Create vector store
    print("\n🔨 Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )
    print(f"✅ Vector store created at: {VECTOR_STORE_PATH}")
    
    return vectorstore


def load_existing_vector_store(embeddings):
    """
    Load existing vector store
    """
    print(f"\n📂 Loading existing vector store from: {VECTOR_STORE_PATH}")
    
    vectorstore = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )
    print("✅ Vector store loaded!")
    return vectorstore


def search_recipes(vectorstore, query, k=3):
    """
    Search for recipes based on query
    """
    print(f"\n🔍 Searching for: '{query}'")
    results = vectorstore.similarity_search(query, k=k)
    
    print(f"\n📋 Found {len(results)} results:")
    print("=" * 60)
    
    for i, doc in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(doc.page_content[:300])
        print(f"Source: Page {doc.metadata.get('page', 'N/A')}")
        print("-" * 60)
    
    return results