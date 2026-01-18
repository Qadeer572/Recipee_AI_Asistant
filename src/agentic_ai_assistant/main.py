import os
from dotenv import load_dotenv
from vector_store import (
    create_embeddings,
    create_vector_store,
    load_existing_vector_store,
    VECTOR_STORE_PATH
)
from rag_chain import (
    create_groq_llm,
    create_rag_chain,
    query_rag_chain
)

load_dotenv()


class RecipeAIAssistant:
    """
    Main Recipe AI Assistant class
    """
    
    def __init__(self, pdf_path=None):
        """
        Initialize the Recipe AI Assistant
        """
        print("\n🍳 Initializing Recipe AI Assistant...")
        print("=" * 60)
        
        # Step 1: Create embeddings
        self.embeddings = create_embeddings()
        
        # Step 2: Load or create vector store
        if os.path.exists(VECTOR_STORE_PATH) and not pdf_path:
            print("\n📂 Loading existing vector store...")
            self.vectorstore = load_existing_vector_store(self.embeddings)
        elif pdf_path:
            print(f"\n📄 Creating new vector store from: {pdf_path}")
            self.vectorstore = create_vector_store(pdf_path, self.embeddings)
        else:
            raise ValueError("No vector store found and no PDF path provided!")
        
        # Step 3: Initialize GROQ LLM
        self.llm = create_groq_llm(
            model_name="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        # Step 4: Create RAG chain
        self.rag_chain = create_rag_chain(self.vectorstore, self.llm)
        
        print("\n✅ Recipe AI Assistant is ready!")
        print("=" * 60)
    
    
    def ask(self, question):
        """
        Ask a question to the Recipe AI
        """
        return query_rag_chain(self.rag_chain, question)
    
    
    def find_recipe_by_name(self, recipe_name):
        """
        Find a specific recipe by name
        """
        question = f"Give me the complete recipe for {recipe_name} including ingredients and step-by-step instructions."
        return self.ask(question)
    
    
    def find_recipes_by_ingredients(self, ingredients):
        """
        Find recipes based on available ingredients
        """
        if isinstance(ingredients, list):
            ingredients = ", ".join(ingredients)
        
        question = f"I have the following ingredients: {ingredients}. What recipes can I make with these? Please suggest 2-3 recipes with complete details."
        return self.ask(question)
    
    
    def interactive_mode(self):
        """
        Interactive chat mode
        """
        print("\n" + "=" * 60)
        print("💬 INTERACTIVE RECIPE ASSISTANT")
        print("=" * 60)
        print("\nCommands:")
        print("  - Type your question naturally")
        print("  - Type 'quit' or 'exit' to end")
        print("  - Type 'help' for example questions")
        print("=" * 60)
        
        while True:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye! Happy cooking!")
                break
            
            if user_input.lower() == 'help':
                self.show_help()
                continue
            
            if not user_input:
                print("⚠️  Please enter a question!")
                continue
            
            # Get response
            self.ask(user_input)
    
    
    def show_help(self):
        """
        Show example questions
        """
        print("\n📋 Example Questions:")
        print("-" * 60)
        print("1. 'Give me a recipe for Chicken Biryani'")
        print("2. 'I have chicken, tomatoes, and rice. What can I make?'")
        print("3. 'Show me a quick pasta recipe'")
        print("4. 'What recipes use eggs and milk?'")
        print("5. 'Give me a vegetarian dinner recipe'")
        print("-" * 60)


def main():
    """
    Main function to run the application
    """
    print("\n" + "=" * 60)
    print("🍳 RECIPE AI ASSISTANT")
    print("=" * 60)
    
    # Check if vector store exists
    if not os.path.exists(VECTOR_STORE_PATH):
        print("\n⚠️  No vector store found!")
        pdf_path = input("Enter the path to your recipe PDF: ").strip()
        
        if not os.path.exists(pdf_path):
            print(f"❌ PDF not found: {pdf_path}")
            return
        
        assistant = RecipeAIAssistant(pdf_path=pdf_path)
    else:
        assistant = RecipeAIAssistant()
    
    # Example usage
    print("\n" + "=" * 60)
    print("🧪 TESTING WITH EXAMPLE QUERIES")
    print("=" * 60)
    
    # Test 1: Find recipe by name
    print("\n--- Test 1: Find Recipe by Name ---")
    assistant.find_recipe_by_name("Chicken Biryani")
    
    # Test 2: Find recipes by ingredients
    print("\n--- Test 2: Find Recipes by Ingredients ---")
    assistant.find_recipes_by_ingredients(["chicken", "tomatoes", "onions"])
    
    # Start interactive mode
    print("\n" + "=" * 60)
    choice = input("\nStart interactive mode? (y/n): ").strip().lower()
    if choice == 'y':
        assistant.interactive_mode()


if __name__ == "__main__":
    main()