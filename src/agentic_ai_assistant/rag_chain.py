import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# Get GROQ API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def create_groq_llm(model_name="llama-3.3-70b-versatile", temperature=0.7):
    """
    Create GROQ LLM instance
    """
    print(f"🤖 Initializing GROQ LLM: {model_name}")
    
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
        max_tokens=1024
    )
    print("✅ GROQ LLM initialized!")
    return llm


def create_recipe_prompt():
    """
    Create custom prompt template for recipe queries
    """
    template = """You are a helpful recipe assistant. Use the following context to answer the user's question about recipes.

Context from recipe book:
{context}

User Question: {question}

Instructions:
- If the user provides ingredients, suggest recipes that use those ingredients
- If the user asks for a specific recipe, provide the complete recipe with ingredients and instructions
- If you don't find relevant information in the context, say so politely
- Be friendly and helpful
- Format your response clearly with sections like Ingredients, Instructions, etc.

Answer:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    return prompt


def create_rag_chain(vectorstore, llm):
    """
    Create RAG chain combining retriever and LLM
    """
    print("\n🔗 Creating RAG chain...")
    
    # Create retriever from vectorstore
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # Return top 4 most relevant chunks
    )
    
    # Create custom prompt
    prompt = create_recipe_prompt()
    
    # Helper function to format documents
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    # Create the RAG chain
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("✅ RAG chain created!")
    return rag_chain


def query_rag_chain(rag_chain, question):
    """
    Query the RAG chain with a question
    """
    print(f"\n{'='*60}")
    print(f"❓ Question: {question}")
    print(f"{'='*60}\n")
    
    try:
        response = rag_chain.invoke(question)
        print(f"🤖 Answer:\n{response}")
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None