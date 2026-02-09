// API Base URL - use relative path
const API_BASE = '/api';

// Global data
let allAttractions = [];
let savedPreferences = null;
let selectedForItinerary = new Set();

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSavedPreferences();
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
            displayAttractions(allAttractions, 'browse-results', true, {});
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

// Display Attractions with Enhanced Cards
function displayAttractions(attractions, containerId, showConversionButtons = true, userPreferences = {}) {
    const container = document.getElementById(containerId);
    
    if (attractions.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:#666;padding:2rem;">No attractions found matching your criteria.</p>';
        return;
    }
    
    container.innerHTML = attractions.map(attr => {
        // Ensure all fields have default values
        attr.num_reviews = attr.num_reviews || attr.num_reviews === 0 ? attr.num_reviews : 'N/A';
        attr.best_season = attr.best_season || 'Year-round';
        attr.duration_days = attr.duration_days !== undefined ? attr.duration_days : 1;
        attr.difficulty = attr.difficulty || 'Moderate';
        attr.avg_cost_usd = attr.avg_cost_usd || 0;
        
        const travelerType = getTravelerType(attr);
        const difficultyExplanation = getDifficultyExplanation(attr.difficulty);
        const totalTripCost = estimateTotalTripCost(attr);
        const isSelected = selectedForItinerary.has(attr.attraction_id);
        
        return `
        <div class="attraction-card enhanced-card" data-id="${attr.attraction_id}">
            <div class="card-header">
                <h3>${attr.name}</h3>
                <label class="itinerary-checkbox">
                    <input type="checkbox" ${isSelected ? 'checked' : ''} 
                           onchange="toggleItinerarySelection(${attr.attraction_id})">
                    <span>Add to itinerary</span>
                </label>
            </div>
            
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
                    <span class="rating">⭐ ${(attr.rating || 0).toFixed(1)}/5.0</span>
                    ${attr.num_reviews !== undefined && attr.num_reviews !== 'N/A' ? 
                        `<span class="info-value">(${attr.num_reviews} reviews)</span>` : 
                        ''}
                </div>
                
                <!-- Enhanced Information -->
                <div class="enhanced-section">
                    <div class="info-row highlight">
                        <span class="info-label">📅 Best Time to Visit:</span>
                        <span class="info-value highlight-value">${attr.best_season}</span>
                    </div>
                    <div class="info-row highlight">
                        <span class="info-label">⏱️ Typical Duration:</span>
                        <span class="info-value highlight-value">${attr.duration_days || 1} ${(attr.duration_days || 1) == 1 ? 'day' : 'days'}</span>
                    </div>
                    <div class="info-row highlight">
                        <span class="info-label">👥 Ideal For:</span>
                        <span class="info-value highlight-value">${travelerType}</span>
                    </div>
                    <div class="info-row highlight">
                        <span class="info-label">💰 Estimated Total Cost:</span>
                        <span class="info-value highlight-value">$${totalTripCost}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Cost per attraction:</span>
                        <span class="info-value">$${attr.avg_cost_usd || 0}</span>
                    </div>
                </div>
                
                <div class="info-row">
                    <span class="info-label">Difficulty:</span>
                    <span class="badge badge-difficulty">${attr.difficulty}</span>
                </div>
                <div class="difficulty-explanation">
                    ${difficultyExplanation}
                </div>
                
                ${attr.similarity_score ? `
                <div class="info-row">
                    <span class="info-label">Match Score:</span>
                    <span class="similarity-score">${(attr.similarity_score * 100).toFixed(0)}%</span>
                </div>
                ` : ''}
                
                <!-- Explanation Section -->
                ${showConversionButtons ? `
                <div class="explanation-section" id="explanation-${attr.attraction_id}">
                    <button class="btn-explanation" onclick="showExplanation(${attr.attraction_id}, ${JSON.stringify(userPreferences).replace(/"/g, '&quot;')})">
                        ℹ️ Why this was recommended
                    </button>
                    <div class="explanation-content" id="explanation-content-${attr.attraction_id}" style="display:none;"></div>
                </div>
                ` : ''}
                
                <!-- Conversion Buttons -->
                ${showConversionButtons ? `
                <div class="conversion-buttons">
                    <button class="btn-conversion btn-email" onclick="requestEmailItinerary([${attr.attraction_id}])">
                        📩 Get by Email
                    </button>
                    <button class="btn-conversion btn-expert" onclick="requestExpertConsultation(${attr.attraction_id})">
                        💬 Talk to Expert
                    </button>
                    <button class="btn-conversion btn-quote" onclick="requestQuote([${attr.attraction_id}])">
                        💵 Get Quote
                    </button>
                </div>
                ` : ''}
            </div>
        </div>
        `;
    }).join('');
}

// Helper functions for enhanced cards
function getTravelerType(attr) {
    const difficulty = attr.difficulty || 'Moderate';
    const category = attr.category || '';
    
    if (difficulty === 'Easy' || difficulty === 'Easy-Moderate') {
        if (category === 'Religious Site' || category === 'Cultural Heritage' || category === 'Market/Shopping') {
            return 'Families, Seniors, All Travelers';
        }
        return 'Families, Couples, Beginners';
    } else if (difficulty === 'Moderate' || difficulty === 'Moderate-Hard') {
        return 'Couples, Solo Travelers, Fit Travelers';
    } else {
        return 'Experienced Trekkers, Adventure Seekers';
    }
}

function getDifficultyExplanation(difficulty) {
    const explanations = {
        'Easy': '🟢 No special fitness required. Suitable for all ages. Mostly flat terrain or easy walks.',
        'Easy-Moderate': '🟡 Light physical activity. Short hikes or moderate walking. Basic fitness recommended.',
        'Moderate': '🟠 Moderate fitness required. Some uphill/downhill walking. 4-6 hours activity per day.',
        'Moderate-Hard': '🔴 Good fitness essential. Challenging terrain, longer hours. Some high altitude.',
        'Hard': '🔴 Very fit travelers only. Strenuous trekking, high altitude, 6-8 hours per day.',
        'Extreme': '⚫ Extreme fitness required. High altitude, technical terrain, professional guidance recommended.'
    };
    return `<p class="difficulty-text">${explanations[difficulty] || 'Difficulty varies'}</p>`;
}

function estimateTotalTripCost(attr) {
    // Estimate total trip cost including accommodation, meals, transport
    const baseCost = parseFloat(attr.avg_cost_usd) || 0;
    const duration = parseFloat(attr.duration_days) || 1;
    
    // Rough estimates: $30/day accommodation + $20/day meals + attraction cost
    const dailyExpenses = 50 * duration;
    const total = baseCost + dailyExpenses;
    
    return Math.round(total);
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
            displayAttractions(data.attractions, 'browse-results', true, {});
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
    displayAttractions(allAttractions, 'browse-results', true, {});
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
            displayAttractions(data.recommendations, 'similar-results', true, {});
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get recommendations.');
    }
    
    hideLoading();
}

// Get or create session ID
function getSessionId() {
    let sessionId = sessionStorage.getItem('session_id');
    if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        sessionStorage.setItem('session_id', sessionId);
    }
    return sessionId;
}

// Preference Memory Functions (now using database)
async function loadSavedPreferences() {
    try {
        // Try loading from database first
        const sessionId = getSessionId();
        const response = await fetch(`${API_BASE}/preferences/load?session_id=${sessionId}`);
        const data = await response.json();
        
        if (data.success && data.preferences) {
            savedPreferences = data.preferences;
            applySavedPreferences();
        } else {
            // Fallback to localStorage
            const saved = localStorage.getItem('nepalRecommenderPreferences');
            if (saved) {
                savedPreferences = JSON.parse(saved);
                applySavedPreferences();
            }
        }
    } catch (e) {
        console.error('Error loading preferences:', e);
        // Fallback to localStorage
        try {
            const saved = localStorage.getItem('nepalRecommenderPreferences');
            if (saved) {
                savedPreferences = JSON.parse(saved);
                applySavedPreferences();
            }
        } catch (e2) {
            console.error('Error loading from localStorage:', e2);
        }
    }
}

async function savePreferences() {
    const prefs = {
        category: document.getElementById('pref-category').value,
        max_cost: document.getElementById('pref-budget').value,
        difficulty: document.getElementById('pref-difficulty').value,
        top_n: document.getElementById('pref-count').value,
        timestamp: new Date().toISOString()
    };
    
    // Save to database
    try {
        const sessionId = getSessionId();
        const response = await fetch(`${API_BASE}/preferences/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                category: prefs.category || null,
                max_cost: prefs.max_cost ? parseFloat(prefs.max_cost) : null,
                difficulty: prefs.difficulty || null,
                regions: []
            })
        });
        
        const data = await response.json();
        if (data.success) {
            savedPreferences = prefs;
        }
    } catch (e) {
        console.error('Error saving preferences to database:', e);
    }
    
    // Also save to localStorage as backup
    try {
        localStorage.setItem('nepalRecommenderPreferences', JSON.stringify(prefs));
    } catch (e) {
        console.error('Error saving to localStorage:', e);
    }
}

function applySavedPreferences() {
    if (!savedPreferences) return;
    
    if (savedPreferences.category) {
        document.getElementById('pref-category').value = savedPreferences.category;
    }
    if (savedPreferences.max_cost) {
        document.getElementById('pref-budget').value = savedPreferences.max_cost;
    }
    if (savedPreferences.difficulty) {
        document.getElementById('pref-difficulty').value = savedPreferences.difficulty;
    }
    if (savedPreferences.top_n) {
        document.getElementById('pref-count').value = savedPreferences.top_n;
    }
}

// Get Preference Recommendations (Enhanced with Memory)
async function getPreferenceRecommendations() {
    showLoading();
    
    const category = document.getElementById('pref-category').value;
    const maxBudget = document.getElementById('pref-budget').value;
    const difficulty = document.getElementById('pref-difficulty').value;
    const topN = document.getElementById('pref-count').value;
    
    // Save preferences
    savePreferences();
    
    const payload = {
        top_n: parseInt(topN)
    };
    
    const userPreferences = {};
    
    if (category) {
        payload.category = category;
        userPreferences.category = category;
    }
    if (maxBudget) {
        payload.max_cost = parseFloat(maxBudget);
        userPreferences.max_cost = parseFloat(maxBudget);
    }
    if (difficulty) {
        payload.difficulty = difficulty;
        userPreferences.difficulty = difficulty;
    }
    
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
            displayAttractions(data.recommendations, 'preferences-results', true, userPreferences);
            
            if (data.count === 0) {
                document.getElementById('preferences-results').innerHTML = 
                    '<p style="text-align:center;color:#666;padding:2rem;">No attractions found matching your preferences. Try adjusting your criteria.</p>';
            } else {
                // Show itinerary generation button if we have results
                const container = document.getElementById('preferences-results');
                const itinerarySection = `
                    <div class="itinerary-section" style="margin-top: 2rem; padding: 1.5rem; background: #f8f9fa; border-radius: 8px;">
                        <h3 style="margin-bottom: 1rem;">📋 Create Trip Itinerary</h3>
                        <p style="margin-bottom: 1rem;">Selected ${selectedForItinerary.size} attraction(s) for your itinerary.</p>
                        <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                            <input type="number" id="itinerary-days" value="5" min="3" max="14" 
                                   style="padding: 0.6rem; border: 1px solid #ddd; border-radius: 5px; width: 150px;"
                                   placeholder="Number of days">
                            <button class="btn btn-primary" onclick="generateItinerary()">
                                🗓️ Generate ${selectedForItinerary.size > 0 ? selectedForItinerary.size : '5'}-Day Itinerary
                            </button>
                            <button class="btn btn-secondary" onclick="clearItinerarySelection()">
                                Clear Selection
                            </button>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', itinerarySection);
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get recommendations.');
    }
    
    hideLoading();
}

// Itinerary Management
function toggleItinerarySelection(attractionId) {
    if (selectedForItinerary.has(attractionId)) {
        selectedForItinerary.delete(attractionId);
    } else {
        selectedForItinerary.add(attractionId);
    }
    
    // Update UI
    const checkbox = document.querySelector(`input[type="checkbox"][onchange*="${attractionId}"]`);
    if (checkbox) {
        checkbox.checked = selectedForItinerary.has(attractionId);
    }
    
    updateItineraryCounter();
}

function clearItinerarySelection() {
    selectedForItinerary.clear();
    document.querySelectorAll('.itinerary-checkbox input[type="checkbox"]').forEach(cb => cb.checked = false);
    updateItineraryCounter();
}

function updateItineraryCounter() {
    const counters = document.querySelectorAll('.itinerary-counter');
    counters.forEach(c => c.textContent = `Selected: ${selectedForItinerary.size}`);
}

// Generate Itinerary
async function generateItinerary() {
    if (selectedForItinerary.size === 0) {
        alert('Please select at least one attraction for your itinerary.');
        return;
    }
    
    showLoading();
    
    const days = parseInt(document.getElementById('itinerary-days')?.value || 5);
    
    try {
        const response = await fetch(`${API_BASE}/itinerary/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                attraction_ids: Array.from(selectedForItinerary),
                days: days,
                start_location: 'Kathmandu'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayItinerary(data.itinerary, data.summary);
        } else {
            alert('Failed to generate itinerary: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate itinerary.');
    }
    
    hideLoading();
}

function displayItinerary(itinerary, summary) {
    const container = document.getElementById('preferences-results');
    
    let html = `
        <div class="itinerary-display" style="margin-top: 2rem;">
            <div class="itinerary-summary" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
                <h2 style="margin-bottom: 1rem;">🗺️ Your ${summary.total_days}-Day Itinerary</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">${summary.total_days}</div>
                        <div>Days</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">$${summary.total_cost}</div>
                        <div>Total Cost</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">$${summary.average_daily_cost}</div>
                        <div>Per Day</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold;">${summary.attractions_count}</div>
                        <div>Attractions</div>
                    </div>
                </div>
                <div style="margin-top: 1rem;">
                    <strong>Regions:</strong> ${summary.regions_covered.join(', ')}
                </div>
            </div>
            
            <div class="itinerary-days">
                ${itinerary.map(day => `
                    <div class="itinerary-day" style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <h3 style="color: #667eea; margin: 0;">Day ${day.day}${day.attraction ? `: ${day.attraction.name}` : ''}</h3>
                            <span class="badge badge-difficulty">${day.difficulty}</span>
                        </div>
                        ${day.attraction ? `
                            <div style="margin-bottom: 1rem;">
                                <div><strong>📍 Location:</strong> ${day.attraction.region}</div>
                                <div><strong>🏷️ Category:</strong> ${day.attraction.category}</div>
                                <div><strong>⏱️ Duration:</strong> ${day.duration} ${day.duration == 1 ? 'day' : 'days'}</div>
                                <div><strong>💰 Cost:</strong> $${day.cost}</div>
                                <div><strong>🌤️ Best Season:</strong> ${day.best_season}</div>
                            </div>
                        ` : ''}
                        <div style="margin-bottom: 1rem;">
                            <strong>Activities:</strong>
                            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                                ${day.activities.map(a => `<li>${a}</li>`).join('')}
                            </ul>
                        </div>
                        ${day.notes.length > 0 ? `
                            <div style="background: #fff3cd; padding: 1rem; border-radius: 5px; border-left: 4px solid #ffc107;">
                                <strong>📌 Notes:</strong>
                                <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                                    ${day.notes.map(n => `<li>${n}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
            
            <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
                <button class="btn btn-primary" onclick="requestEmailItinerary(Array.from(selectedForItinerary))">
                    📩 Email This Itinerary
                </button>
                <button class="btn btn-primary" onclick="requestExpertConsultation(null)">
                    💬 Get Expert Consultation
                </button>
                <button class="btn btn-primary" onclick="requestQuote(Array.from(selectedForItinerary))">
                    💵 Request Custom Quote
                </button>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

// Explanation Functions
async function showExplanation(attractionId, userPreferences) {
    const contentDiv = document.getElementById(`explanation-content-${attractionId}`);
    
    if (contentDiv.style.display === 'none' || !contentDiv.innerHTML) {
        showLoading();
        
        try {
            const response = await fetch(`${API_BASE}/recommend/explain`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    attraction_id: attractionId,
                    preferences: userPreferences
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                contentDiv.innerHTML = `
                    <div style="background: #e3f2fd; padding: 1rem; border-radius: 5px; margin-top: 0.5rem; border-left: 4px solid #2196F3;">
                        <strong>Why we recommended "${data.attraction.name}":</strong>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            ${data.explanations.map(exp => `<li>${exp}</li>`).join('')}
                        </ul>
                    </div>
                `;
                contentDiv.style.display = 'block';
            }
        } catch (error) {
            console.error('Error:', error);
            contentDiv.innerHTML = '<p style="color: red;">Failed to load explanation.</p>';
            contentDiv.style.display = 'block';
        }
        
        hideLoading();
    } else {
        contentDiv.style.display = contentDiv.style.display === 'none' ? 'block' : 'none';
    }
}

// Conversion Request Functions
async function requestEmailItinerary(attractionIds) {
    if (attractionIds.length === 0) {
        attractionIds = Array.from(selectedForItinerary);
    }
    
    if (attractionIds.length === 0) {
        alert('Please select attractions for your itinerary first.');
        return;
    }
    
    const email = prompt('Please enter your email address:');
    if (!email) return;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/conversion/request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: 'email',
                user_data: { email: email },
                attraction_ids: attractionIds
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to send request.');
    }
    
    hideLoading();
}

async function requestExpertConsultation(attractionId) {
    const name = prompt('Please enter your name:');
    if (!name) return;
    
    const contact = prompt('Please enter your email or phone:');
    if (!contact) return;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/conversion/request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: 'expert',
                user_data: { name: name, contact: contact },
                attraction_ids: attractionId ? [attractionId] : Array.from(selectedForItinerary)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to send request.');
    }
    
    hideLoading();
}

async function requestQuote(attractionIds) {
    if (attractionIds.length === 0) {
        attractionIds = Array.from(selectedForItinerary);
    }
    
    if (attractionIds.length === 0) {
        alert('Please select attractions first.');
        return;
    }
    
    const name = prompt('Please enter your name:');
    if (!name) return;
    
    const email = prompt('Please enter your email:');
    if (!email) return;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/conversion/request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: 'quote',
                user_data: { name: name, email: email },
                attraction_ids: attractionIds
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to send request.');
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