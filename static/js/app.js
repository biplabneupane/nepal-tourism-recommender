// API Base URL - use relative path
const API_BASE = '/api';

// Global data
let allAttractions = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadInitialData();
    loadStats();
});

// Tab Management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Activate button
    event.target.classList.add('active');
}

// Loading Overlay
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Load Initial Data
async function loadInitialData() {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/attractions`);
        const data = await response.json();
        
        if (data.success) {
            allAttractions = data.attractions;
            
            // Populate filters
            populateFilters();
            
            // Populate similar dropdown
            populateSimilarDropdown();
            
            // Display attractions
            displayAttractions(allAttractions, 'browse-results');
        }
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Failed to load attractions. Please refresh the page.');
    }
    
    hideLoading();
}

// Populate Filter Dropdowns
function populateFilters() {
    const categories = [...new Set(allAttractions.map(a => a.category))].sort();
    const regions = [...new Set(allAttractions.map(a => a.region))].sort();
    
    const categorySelect = document.getElementById('filter-category');
    const regionSelect = document.getElementById('filter-region');
    const prefCategorySelect = document.getElementById('pref-category');
    
    categories.forEach(cat => {
        categorySelect.add(new Option(cat, cat));
        prefCategorySelect.add(new Option(cat, cat));
    });
    
    regions.forEach(region => {
        regionSelect.add(new Option(region, region));
    });
}

// Populate Similar Dropdown
function populateSimilarDropdown() {
    const select = document.getElementById('similar-attraction');
    
    allAttractions
        .sort((a, b) => b.rating - a.rating)
        .forEach(attr => {
            const option = new Option(
                `${attr.name} (${attr.category})`,
                attr.attraction_id
            );
            select.add(option);
        });
}

// Display Attractions
function displayAttractions(attractions, containerId) {
    const container = document.getElementById(containerId);
    
    if (attractions.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:2rem;">No attractions found matching your criteria.</p>';
        return;
    }
    
    container.innerHTML = attractions.map(attr => `
        <div class="attraction-card">
            <h3>${attr.name}</h3>
            <div class="attraction-info">
                <div class="info-row">
                    <span class="info-label">Category:</span>
                    <span class="badge badge-category">${attr.category}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Region:</span>
                    <span class="info-value">${attr.region}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Rating:</span>
                    <span class="rating">⭐ ${attr.rating.toFixed(1)}/5.0</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Reviews:</span>
                    <span class="info-value">${attr.num_reviews}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Cost:</span>
                    <span class="info-value">$${attr.avg_cost_usd}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Duration:</span>
                    <span class="info-value">${attr.duration_days} days</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Difficulty:</span>
                    <span class="badge badge-difficulty">${attr.difficulty}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Best Season:</span>
                    <span class="info-value">${attr.best_season}</span>
                </div>
                ${attr.similarity_score ? `
                <div class="info-row">
                    <span class="info-label">Similarity:</span>
                    <span class="similarity-score">${(attr.similarity_score * 100).toFixed(0)}%</span>
                </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Apply Filters
async function applyFilters() {
    showLoading();
    
    const category = document.getElementById('filter-category').value;
    const region = document.getElementById('filter-region').value;
    const maxCost = document.getElementById('filter-cost').value;
    const minRating = document.getElementById('filter-rating').value;
    
    let url = `${API_BASE}/attractions?`;
    if (category) url += `category=${category}&`;
    if (region) url += `region=${region}&`;
    if (maxCost) url += `max_cost=${maxCost}&`;
    if (minRating) url += `min_rating=${minRating}&`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            displayAttractions(data.attractions, 'browse-results');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to filter attractions.');
    }
    
    hideLoading();
}

// Clear Filters
function clearFilters() {
    document.getElementById('filter-category').value = '';
    document.getElementById('filter-region').value = '';
    document.getElementById('filter-cost').value = '';
    document.getElementById('filter-rating').value = '';
    displayAttractions(allAttractions, 'browse-results');
}

// Find Similar
async function findSimilar() {
    const attractionId = document.getElementById('similar-attraction').value;
    const topN = document.getElementById('similar-count').value;
    
    if (!attractionId) {
        alert('Please select an attraction first.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/recommend/similar/${attractionId}?top_n=${topN}`);
        const data = await response.json();
        
        if (data.success) {
            // Display original
            const originalDiv = document.getElementById('similar-original');
            originalDiv.innerHTML = `
                <h3>You selected: ${data.original.name}</h3>
                <p>Category: ${data.original.category} | Region: ${data.original.region}</p>
                <p style="margin-top:0.5rem;">Based on this, here are similar attractions you might enjoy:</p>
            `;
            
            // Display recommendations
            displayAttractions(data.recommendations, 'similar-results');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get recommendations.');
    }
    
    hideLoading();
}

// Get Preference Recommendations
async function getPreferenceRecommendations() {
    showLoading();
    
    const category = document.getElementById('pref-category').value;
    const maxBudget = document.getElementById('pref-budget').value;
    const difficulty = document.getElementById('pref-difficulty').value;
    const topN = document.getElementById('pref-count').value;
    
    const payload = {
        top_n: parseInt(topN)
    };
    
    if (category) payload.category = category;
    if (maxBudget) payload.max_cost = parseFloat(maxBudget);
    if (difficulty) payload.difficulty = difficulty;
    
    try {
        const response = await fetch(`${API_BASE}/recommend/preferences`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayAttractions(data.recommendations, 'preferences-results');
            
            if (data.count === 0) {
                document.getElementById('preferences-results').innerHTML = 
                    '<p style="text-align:center;color:#666;padding:2rem;">No attractions found matching your preferences. Try adjusting your criteria.</p>';
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get recommendations.');
    }
    
    hideLoading();
}

// Load Statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        if (data.success) {
            displayStats(data.stats);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Display Statistics
function displayStats(stats) {
    const container = document.getElementById('stats-content');
    
    // Create stat cards
    let html = `
        <div class="stat-card">
            <h3>${stats.total_attractions}</h3>
            <p>Total Attractions</p>
        </div>
        
        <div class="stat-card">
            <h3>${stats.avg_rating.toFixed(2)}</h3>
            <p>Average Rating</p>
        </div>
        
        <div class="stat-card">
            <h3>$${stats.avg_cost.toFixed(0)}</h3>
            <p>Average Cost</p>
        </div>
        
        <div class="stat-card">
            <h3>$${stats.cost_range.min} - $${stats.cost_range.max}</h3>
            <p>Cost Range</p>
        </div>
    `;
    
    // Add category breakdown
    html += `
        <div class="chart-container" style="grid-column: 1 / -1;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Attractions by Category</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                ${Object.entries(stats.categories)
                    .sort((a, b) => b[1] - a[1])
                    .map(([category, count]) => `
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; text-align: center;">
                            <div style="font-size: 2rem; font-weight: bold; color: #667eea;">${count}</div>
                            <div style="color: #666; margin-top: 0.5rem;">${category}</div>
                        </div>
                    `).join('')}
            </div>
        </div>
    `;
    
    // Add region breakdown
    html += `
        <div class="chart-container" style="grid-column: 1 / -1;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">Attractions by Region</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                ${Object.entries(stats.regions)
                    .sort((a, b) => b[1] - a[1])
                    .map(([region, count]) => `
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; text-align: center;">
                            <div style="font-size: 2rem; font-weight: bold; color: #764ba2;">${count}</div>
                            <div style="color: #666; margin-top: 0.5rem;">${region}</div>
                        </div>
                    `).join('')}
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}