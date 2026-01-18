// ==================== State Management ====================
let currentSearchType = 'recipe';

// ==================== DOM Elements ====================
const recipeBtn = document.getElementById('recipeBtn');
const ingredientsBtn = document.getElementById('ingredientsBtn');
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const searchHint = document.getElementById('searchHint');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');
const resultsTitle = document.getElementById('resultsTitle');
const closeResults = document.getElementById('closeResults');

// ==================== Event Listeners ====================
recipeBtn.addEventListener('click', () => setSearchType('recipe'));
ingredientsBtn.addEventListener('click', () => setSearchType('ingredients'));
searchForm.addEventListener('submit', handleSearch);
closeResults.addEventListener('click', hideResults);

// ==================== Functions ====================

/**
 * Set the search type (recipe or ingredients)
 */
function setSearchType(type) {
    currentSearchType = type;

    // Update button states
    if (type === 'recipe') {
        recipeBtn.classList.add('active');
        ingredientsBtn.classList.remove('active');
        searchInput.placeholder = 'Enter recipe name (e.g., Chicken Biryani)';
        searchHint.textContent = 'Try: "Chicken Biryani", "Pasta Carbonara", "Chocolate Cake"';
    } else {
        ingredientsBtn.classList.add('active');
        recipeBtn.classList.remove('active');
        searchInput.placeholder = 'Enter ingredients (e.g., chicken, tomatoes, rice)';
        searchHint.textContent = 'Try: "chicken, tomatoes, rice" or "eggs, milk, flour"';
    }

    // Clear input and results
    searchInput.value = '';
    hideResults();
}

/**
 * Handle search form submission
 */
async function handleSearch(e) {
    e.preventDefault();

    const query = searchInput.value.trim();

    if (!query) {
        showError('Please enter a search query');
        return;
    }

    // Show loading state
    setLoading(true);
    hideResults();

    try {
        const response = await fetch('/api/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                type: currentSearchType
            })
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred while searching');
        }
    } catch (error) {
        console.error('Search error:', error);
        showError('Failed to connect to the server. Please try again.');
    } finally {
        setLoading(false);
    }
}

/**
 * Display search results with formatted recipe cards
 */
function displayResults(data) {
    const resultText = data.result || 'No results found';

    // Update title based on search type
    if (currentSearchType === 'recipe') {
        resultsTitle.textContent = `Recipe: ${data.query}`;
    } else {
        resultsTitle.textContent = `Recipes with: ${data.query}`;
    }

    // Parse and format the result
    const formattedHTML = parseRecipe(resultText);

    // Display results
    resultsContent.innerHTML = formattedHTML;
    resultsSection.style.display = 'block';

    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Parse AI response and create formatted recipe HTML
 */
function parseRecipe(text) {
    // Split into multiple recipes if present (for ingredient search)
    const recipes = text.split(/(?=Recipe \d+:|^\d+\.\s+\*\*)/m);

    let html = '';

    recipes.forEach((recipeText, index) => {
        if (!recipeText.trim()) return;

        // Extract recipe name
        const nameMatch = recipeText.match(/(?:Recipe Name:|^\d+\.\s+\*\*|Recipe \d+:)\s*(.+?)(?:\n|$)/i);
        const recipeName = nameMatch ? nameMatch[1].replace(/\*\*/g, '').trim() : `Recipe ${index + 1}`;

        // Extract ingredients
        const ingredientsMatch = recipeText.match(/(?:Ingredients?|Required Ingredients?)[\s:]*\n([\s\S]*?)(?=\n\n|Instructions?|Preparation|Steps|Important|$)/i);
        const ingredientsText = ingredientsMatch ? ingredientsMatch[1] : '';
        const ingredients = extractListItems(ingredientsText);

        // Extract instructions
        const instructionsMatch = recipeText.match(/(?:Instructions?|Steps|Preparation|Method)[\s:]*\n([\s\S]*?)(?=\n\n|Important|Notes|Tips|$)/i);
        const instructionsText = instructionsMatch ? instructionsMatch[1] : '';
        const instructions = extractListItems(instructionsText);

        // Extract important notes
        const notesMatch = recipeText.match(/(?:Important Notes?|Tips?|Notes?)[\s:]*\n([\s\S]*?)$/i);
        const notes = notesMatch ? notesMatch[1].trim() : '';

        // Build HTML for this recipe
        html += buildRecipeCard(recipeName, ingredients, instructions, notes);

        // Add separator if multiple recipes
        if (index < recipes.length - 1 && recipes.length > 1) {
            html += '<div class="recipe-separator"></div>';
        }
    });

    // If parsing failed, show raw text in a nice format
    if (!html.trim()) {
        html = `<div class="recipe-card"><div class="notes-content">${text.replace(/\n/g, '<br>')}</div></div>`;
    }

    return html;
}

/**
 * Extract list items from text
 */
function extractListItems(text) {
    if (!text) return [];

    const lines = text.split('\n');
    const items = [];

    lines.forEach(line => {
        line = line.trim();
        // Match numbered lists, bullet points, or dashes
        const match = line.match(/^(?:\d+[\.)]\s*|[-•*]\s*)(.+)/);
        if (match) {
            items.push(match[1].trim());
        } else if (line && !line.match(/^(?:Ingredients?|Instructions?|Steps|Notes?|Tips?)/i)) {
            items.push(line);
        }
    });

    return items.filter(item => item.length > 0);
}

/**
 * Build HTML for a recipe card
 */
function buildRecipeCard(name, ingredients, instructions, notes) {
    let html = '<div class="recipe-card">';

    // Recipe Name
    html += `<h2 class="recipe-name">${escapeHtml(name)}</h2>`;

    // Ingredients
    if (ingredients.length > 0) {
        html += '<div class="ingredients-box">';
        html += '<div class="section-header">INGREDIENTS:</div>';
        html += '<ul class="ingredients-list">';
        ingredients.forEach(ingredient => {
            html += `<li>${escapeHtml(ingredient)}</li>`;
        });
        html += '</ul>';
        html += '</div>';
    }

    // Instructions
    if (instructions.length > 0) {
        html += '<div class="instructions-box">';
        html += '<div class="section-header">INSTRUCTIONS:</div>';
        html += '<ol class="instructions-list">';
        instructions.forEach(instruction => {
            html += `<li>${escapeHtml(instruction)}</li>`;
        });
        html += '</ol>';
        html += '</div>';
    }

    // Important Notes
    if (notes) {
        html += '<div class="notes-box">';
        html += '<div class="section-header">IMPORTANT NOTES:</div>';
        html += `<div class="notes-content">${escapeHtml(notes).replace(/\n/g, '<br>')}</div>`;
        html += '</div>';
    }

    html += '</div>';
    return html;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Hide results section
 */
function hideResults() {
    resultsSection.style.display = 'none';
}

/**
 * Set loading state
 */
function setLoading(isLoading) {
    const btnText = searchBtn.querySelector('.btn-text');
    const btnLoader = searchBtn.querySelector('.btn-loader');

    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        searchBtn.disabled = true;
        searchInput.disabled = true;
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        searchBtn.disabled = false;
        searchInput.disabled = false;
    }
}

/**
 * Show error message
 */
function showError(message) {
    resultsTitle.textContent = 'Error';
    resultsContent.innerHTML = `
        <div class="error-message">
            <strong>⚠️ Error:</strong> ${escapeHtml(message)}
        </div>
    `;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ==================== Initialize ====================
console.log('Recipe AI Assistant loaded successfully! 🍳');

// Check API health on load
fetch('/api/health/')
    .then(response => response.json())
    .then(data => {
        console.log('API Health:', data);
    })
    .catch(error => {
        console.error('API Health Check Failed:', error);
    });
