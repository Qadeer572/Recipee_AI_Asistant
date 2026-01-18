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
 * Display search results
 */
function displayResults(data) {
    const resultText = data.result || 'No results found';

    // Format the result text
    const formattedResult = formatResult(resultText);

    // Update title based on search type
    if (currentSearchType === 'recipe') {
        resultsTitle.textContent = `Recipe: ${data.query}`;
    } else {
        resultsTitle.textContent = `Recipes with: ${data.query}`;
    }

    // Display results
    resultsContent.innerHTML = formattedResult;
    resultsSection.style.display = 'block';

    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Format the result text with HTML
 */
function formatResult(text) {
    // Split by double newlines to get sections
    let formatted = text
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');

    // Bold section headers (lines ending with :)
    formatted = formatted.replace(/^(.+:)$/gm, '<strong>$1</strong>');

    // Highlight recipe names (assuming they're in quotes or start with numbers)
    formatted = formatted.replace(/(\d+\.\s+)([^<\n]+)/g, '$1<strong style="color: var(--primary-color);">$2</strong>');

    return formatted;
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
            <strong>⚠️ Error:</strong> ${message}
        </div>
    `;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Show success message
 */
function showSuccess(message) {
    resultsContent.innerHTML = `
        <div class="success-message">
            <strong>✓ Success:</strong> ${message}
        </div>
    `;
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
