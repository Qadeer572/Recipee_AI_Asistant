# Recipe AI Assistant - Django Web Application

🍳 **AI-Powered Recipe Search Application** built with Django, LangChain, Groq, and RAG (Retrieval-Augmented Generation).

## 🌟 Features

- **Smart Recipe Search**: Search by recipe name or available ingredients
- **AI-Powered Responses**: Uses Groq's Llama 3.3 70B model for intelligent recipe suggestions
- **RAG Technology**: Retrieval-Augmented Generation ensures accurate, context-aware responses
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Search History**: Track your recipe searches
- **REST API**: Full-featured API for recipe search

## 🏗️ Project Structure

```
recipee_ai/
├── recipe_project/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── recipe_app/              # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── ai_service.py       # AI/RAG integration
├── src/agentic_ai_assistant/  # Core AI logic
│   ├── main.py             # CLI interface
│   ├── vector_store.py     # Vector database management
│   ├── rag_chain.py        # RAG chain implementation
│   └── pdf_processor.py    # PDF processing
├── templates/               # HTML templates
│   └── home.html
├── static/                  # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── data/                    # Recipe PDF data
├── vectorstore/             # Vector database storage
├── manage.py                # Django management script
├── pyproject.toml           # Poetry dependencies
└── .env                     # Environment variables
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- Groq API Key

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd recipee_ai
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Set up environment variables**:
   - The `.env` file should already contain your `GROQ_API_KEY`
   - Optionally add `DJANGO_SECRET_KEY` for production

4. **Create vector store** (if not already created):
   ```bash
   poetry run python src/agentic_ai_assistant/main.py
   # Follow prompts to load your recipe PDF
   ```

5. **Run database migrations**:
   ```bash
   poetry run python manage.py migrate
   ```

6. **Create a superuser** (optional, for admin access):
   ```bash
   poetry run python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   poetry run python manage.py runserver
   ```

8. **Open your browser**:
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📡 API Endpoints

### 1. Search Recipe
**POST** `/api/search/`

Request body:
```json
{
  "query": "Chicken Biryani",
  "type": "recipe"
}
```

Response:
```json
{
  "success": true,
  "query": "Chicken Biryani",
  "query_type": "recipe",
  "result": "Recipe details..."
}
```

### 2. Search by Ingredients
**POST** `/api/search/`

Request body:
```json
{
  "query": "chicken, tomatoes, rice",
  "type": "ingredients"
}
```

### 3. Get Search History
**GET** `/api/history/`

Response:
```json
{
  "history": [
    {
      "id": 1,
      "query_type": "recipe",
      "query_text": "Chicken Biryani",
      "created_at": "2026-01-19T00:00:00Z"
    }
  ]
}
```

### 4. Health Check
**GET** `/api/health/`

Response:
```json
{
  "status": "healthy",
  "ai_service": "initialized"
}
```

## 🎨 Frontend Features

- **Search Type Toggle**: Switch between recipe name and ingredient search
- **Real-time Search**: Instant results with loading indicators
- **Formatted Results**: Clean, readable recipe display
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Modern UI with transitions and effects

## 🛠️ Technology Stack

### Backend
- **Django 5.2**: Web framework
- **Django REST Framework**: API development
- **LangChain**: AI orchestration
- **Groq**: LLM provider (Llama 3.3 70B)
- **ChromaDB**: Vector database
- **HuggingFace**: Embeddings (sentence-transformers)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (Vanilla)**: Interactive functionality
- **Google Fonts (Inter)**: Typography

### AI/ML
- **RAG (Retrieval-Augmented Generation)**: Context-aware responses
- **Vector Embeddings**: Semantic search
- **PDF Processing**: Recipe book ingestion

## 📝 Usage Examples

### Web Interface

1. **Search by Recipe Name**:
   - Select "Search by Recipe Name"
   - Enter: "Chicken Biryani"
   - Click "Search"
   - View complete recipe with ingredients and instructions

2. **Search by Ingredients**:
   - Select "Search by Ingredients"
   - Enter: "chicken, tomatoes, onions"
   - Click "Search"
   - View suggested recipes using those ingredients

### API Usage (cURL)

```bash
# Search by recipe name
curl -X POST http://127.0.0.1:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "Chicken Biryani", "type": "recipe"}'

# Search by ingredients
curl -X POST http://127.0.0.1:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "chicken, rice, tomatoes", "type": "ingredients"}'
```

## 🔧 Configuration

### Environment Variables

Create or update `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
DJANGO_SECRET_KEY=your_secret_key_here
```

### Django Settings

Key settings in `recipe_project/settings.py`:
- `DEBUG = True` (set to False in production)
- `ALLOWED_HOSTS = ['*']` (restrict in production)
- `CORS_ALLOW_ALL_ORIGINS = True` (configure for production)

## 📦 Dependencies

Main dependencies (see `pyproject.toml` for full list):
- django ^5.1
- djangorestframework ^3.15
- django-cors-headers ^4.6
- langchain
- langchain-groq
- langchain-huggingface
- sentence-transformers
- chromadb
- pypdf ^6.6.0

## 🚀 Deployment

### Production Checklist

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set strong `SECRET_KEY`
4. Configure CORS properly
5. Use production database (PostgreSQL recommended)
6. Collect static files: `python manage.py collectstatic`
7. Use production server (Gunicorn, uWSGI)
8. Set up HTTPS
9. Configure environment variables securely

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Built with ❤️ using Django, LangChain, and Groq

## 🙏 Acknowledgments

- **Groq**: For providing fast LLM inference
- **LangChain**: For the AI orchestration framework
- **HuggingFace**: For embedding models
- **Django**: For the robust web framework

---

**Happy Cooking! 🍳**
