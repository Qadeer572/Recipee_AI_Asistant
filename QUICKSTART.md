# Quick Start Guide - Recipe AI Web Application

## ✅ Setup Complete!

Your Django web application is ready to use!

## 🚀 How to Run

### Option 1: Using the Batch Script (Easiest)
```bash
start_server.bat
```

### Option 2: Using Poetry Command
```bash
poetry run python manage.py runserver
```

## 🌐 Access the Application

Once the server is running, open your browser and visit:

**Main Application**: http://127.0.0.1:8000/

**Admin Panel**: http://127.0.0.1:8000/admin/
(You'll need to create a superuser first - see below)

## 📋 First Time Setup Checklist

- [x] Dependencies installed
- [x] Database migrated
- [x] Vector store created (from Recipe-Book.pdf)
- [x] Environment variables configured
- [ ] Create superuser (optional)

## 👤 Create Admin User (Optional)

To access the Django admin panel:

```bash
poetry run python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## 🎯 How to Use

### Web Interface

1. **Search by Recipe Name**:
   - Click "Search by Recipe Name"
   - Enter a recipe name (e.g., "Chicken Biryani")
   - Click "Search"
   - View the complete recipe with ingredients and instructions

2. **Search by Ingredients**:
   - Click "Search by Ingredients"
   - Enter your available ingredients (e.g., "chicken, tomatoes, rice")
   - Click "Search"
   - View suggested recipes you can make

### API Testing

Test the API using curl or Postman:

```bash
# Health check
curl http://127.0.0.1:8000/api/health/

# Search by recipe name
curl -X POST http://127.0.0.1:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Chicken Biryani\", \"type\": \"recipe\"}"

# Search by ingredients
curl -X POST http://127.0.0.1:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"chicken, rice, tomatoes\", \"type\": \"ingredients\"}"
```

## 🔧 Troubleshooting

### Server won't start?
- Make sure port 8000 is not in use
- Check that all dependencies are installed: `poetry install`
- Verify the vector store exists in `vectorstore/recipe_db/`

### AI not responding?
- Check your GROQ_API_KEY in `.env` file
- Verify the vector store was created successfully
- Check the console for error messages

### Can't find recipes?
- Ensure the Recipe-Book.pdf was processed correctly
- Try different search terms
- Check that the vector store contains data

## 📁 Project Structure

```
recipee_ai/
├── recipe_project/      # Django settings
├── recipe_app/          # Main app (views, models, URLs)
├── templates/           # HTML templates
├── static/              # CSS, JavaScript
├── data/                # Recipe PDF
├── vectorstore/         # AI vector database
├── manage.py            # Django management
└── start_server.bat     # Quick start script
```

## 🎨 Features

✅ Modern, responsive UI
✅ AI-powered recipe search
✅ Search by recipe name or ingredients
✅ Complete recipe details with instructions
✅ Search history tracking
✅ REST API for integration
✅ Admin panel for management

## 📚 Documentation

For detailed documentation, see `README.md`

## 🆘 Need Help?

- Check the console output for error messages
- Review the README.md for detailed information
- Ensure all environment variables are set correctly

---

**Enjoy cooking with AI! 🍳**
