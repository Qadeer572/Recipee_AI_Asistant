"""
Recipe AI Service - Integrates with the existing RAG system
"""
import os
from pathlib import Path
import sys

# Add the src directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_PATH = BASE_DIR / 'src' / 'agentic_ai_assistant'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

try:
    from vector_store import (
        create_embeddings,
        load_existing_vector_store,
        VECTOR_STORE_PATH
    )
    from rag_chain import (
        create_groq_llm,
        create_rag_chain,
    )
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Python path: {sys.path}")
    print(f"SRC_PATH: {SRC_PATH}")
    raise


class RecipeAIService:
    """
    Singleton service for Recipe AI
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialize()
            RecipeAIService._initialized = True

    def _initialize(self):
        """Initialize the AI components"""
        print("🔧 Initializing Recipe AI Service...")
        
        # Check if vector store exists
        if not os.path.exists(VECTOR_STORE_PATH):
            raise FileNotFoundError(
                f"Vector store not found at {VECTOR_STORE_PATH}. "
                "Please run the CLI tool first to create the vector store."
            )
        
        # Load embeddings
        self.embeddings = create_embeddings()
        
        # Load vector store
        self.vectorstore = load_existing_vector_store(self.embeddings)
        
        # Initialize LLM
        self.llm = create_groq_llm(
            model_name="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        # Create RAG chain
        self.rag_chain = create_rag_chain(self.vectorstore, self.llm)
        
        print("✅ Recipe AI Service initialized!")

    def search_by_recipe_name(self, recipe_name: str) -> dict:
        """
        Search for a recipe by name
        Returns: dict with recipe details
        """
        try:
            question = f"""Give me the complete recipe for {recipe_name}. 
            
            Please provide:
            1. Recipe Name
            2. Ingredients (list each ingredient with measurements)
            3. Step-by-step Instructions
            4. Important Notes or Tips (if any)
            
            Format the response clearly with sections."""
            
            response = self.rag_chain.invoke(question)
            
            return {
                'success': True,
                'query': recipe_name,
                'query_type': 'recipe_name',
                'result': response
            }
        except Exception as e:
            return {
                'success': False,
                'query': recipe_name,
                'query_type': 'recipe_name',
                'error': str(e)
            }

    def search_by_ingredients(self, ingredients: str) -> dict:
        """
        Search for recipes by ingredients
        Returns: dict with recipe suggestions
        """
        try:
            question = f"""I have the following ingredients: {ingredients}
            
            Please suggest 2-3 recipes I can make with these ingredients.
            
            For each recipe, provide:
            1. Recipe Name
            2. Required Ingredients (highlight which ones I already have)
            3. Brief Instructions
            4. Important Notes
            
            Format the response clearly with sections for each recipe."""
            
            response = self.rag_chain.invoke(question)
            
            return {
                'success': True,
                'query': ingredients,
                'query_type': 'ingredients',
                'result': response
            }
        except Exception as e:
            return {
                'success': False,
                'query': ingredients,
                'query_type': 'ingredients',
                'error': str(e)
            }

    def general_query(self, question: str) -> dict:
        """
        Handle general recipe-related queries
        """
        try:
            response = self.rag_chain.invoke(question)
            
            return {
                'success': True,
                'query': question,
                'query_type': 'general',
                'result': response
            }
        except Exception as e:
            return {
                'success': False,
                'query': question,
                'query_type': 'general',
                'error': str(e)
            }


# Global instance
recipe_ai_service = None

def get_recipe_ai_service():
    """Get or create the Recipe AI Service instance"""
    global recipe_ai_service
    if recipe_ai_service is None:
        recipe_ai_service = RecipeAIService()
    return recipe_ai_service
