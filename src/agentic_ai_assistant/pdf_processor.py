import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

def extract_recipes_from_pdf(pdf_path):
    """
    Extract text from PDF file
    """
    try:
        # Method 1: Using PyPDFLoader (LangChain)
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        print(f"📄 Loaded {len(pages)} pages from PDF")
        
        # Combine all pages
        full_text = "\n\n".join([page.page_content for page in pages])
        
        return pages, full_text
    
    except Exception as e:
        print(f"❌ Error loading PDF: {e}")
        return None, None


def split_into_chunks(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into smaller chunks for better retrieval
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"📦 Created {len(chunks)} chunks from documents")
    
    return chunks


def process_recipe_pdf(pdf_path):
    """
    Main function to process recipe PDF
    """
    print(f"🔍 Processing: {pdf_path}")
    
    # Extract text
    pages, full_text = extract_recipes_from_pdf(pdf_path)
    
    if not pages:
        return None
    
    # Split into chunks
    chunks = split_into_chunks(pages)
    
    # Preview first chunk
    print("\n📋 Preview of first chunk:")
    print("-" * 50)
    print(chunks[0].page_content[:300])
    print("-" * 50)
    
    return chunks


# Example usage
if __name__ == "__main__":
    # Replace with your PDF file path
    pdf_file = "data/Recipe-Book.pdf"
    
    if os.path.exists(pdf_file):
        chunks = process_recipe_pdf(pdf_file)
        print(f"\n✅ Successfully processed {len(chunks)} recipe chunks")
    else:
        print(f"❌ PDF file not found: {pdf_file}")
        print("📁 Please place your recipe PDF in the 'data' folder")