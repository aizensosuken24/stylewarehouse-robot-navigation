/**
 * Main Application Logic
 */

// Global state
const state = {
    catalogue: [],
    selectedItems: [],
    currentSimulation: null,
};

// DOM elements
const elements = {
    // Catalogue
    searchInput: document.getElementById('search-input'),
    searchBtn: document.getElementById('search-btn'),
    clearBtn: document.getElementById('clear-btn'),
    catalogueResults: document.getElementById('catalogue-results'),

    // Order
    demoBtn: document.getElementById('demo-btn'),
    simulateBtn: document.getElementById('simulate-btn'),
    clearOrderBtn: document.getElementById('clear-order-btn'),
    orderList: document.getElementById('order-list'),
    orderSummary: document.getElementById('order-summary'),

    // Visualization
    canvas: document.getElementById('warehouse-canvas'),
    statsDistance: document.getElementById('stat-distance'),
    statsItems: document.getElementById('stat-items'),
    statsWaypoints: document.getElementById('stat-waypoints'),
    pathfindingDetails: document.getElementById('pathfinding-details'),

    // Response
    responseData: document.getElementById('response-data'),

    // Status
    healthStatus: document.getElementById('health-status'),
};

let visualizer = null;

/**
 * Initialize the application
 */
async function init() {
    console.log('Initializing application...');

    try {
        // Setup event listeners
        setupEventListeners();

        // Check API health
        await checkHealth();

        // Initialize visualizer
        visualizer = new WarehouseVisualizer('warehouse-canvas');

        // Load catalogue
        await loadCatalogue();
        
        console.log('Application initialized successfully');
    } catch (error) {
        console.error('Fatal error during initialization:', error);
        alert('Failed to initialize application. Check console for details.');
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    elements.searchBtn.addEventListener('click', () => searchCatalogue());
    elements.clearBtn.addEventListener('click', () => clearSearch());
    elements.searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchCatalogue();
    });

    elements.demoBtn.addEventListener('click', () => loadDemoOrder());
    elements.simulateBtn.addEventListener('click', () => runSimulation());
    elements.clearOrderBtn.addEventListener('click', () => clearOrder());
}

/**
 * Check API health status
 */
async function checkHealth() {
    try {
        const isHealthy = await API.health();
        updateHealthStatus(isHealthy);
    } catch (error) {
        console.error('Health check error:', error);
        updateHealthStatus(false);
    }
}

/**
 * Update health status indicator
 */
function updateHealthStatus(isHealthy) {
    const statusEl = elements.healthStatus;
    if (isHealthy) {
        statusEl.textContent = '● Connected';
        statusEl.classList.add('online');
        statusEl.classList.remove('offline');
    } else {
        statusEl.textContent = '● Disconnected';
        statusEl.classList.add('offline');
        statusEl.classList.remove('online');
    }
}

/**
 * Load the full catalogue
 */
async function loadCatalogue() {
    try {
        showLoading(elements.catalogueResults);
        const data = await API.getCatalogue();
        state.catalogue = data.items || data || [];
        displayCatalogue(state.catalogue);
    } catch (error) {
        showError(elements.catalogueResults, 'Failed to load catalogue');
        console.error(error);
    }
}

/**
 * Search the catalogue
 */
async function searchCatalogue() {
    const query = elements.searchInput.value.trim();
    if (!query) {
        await loadCatalogue();
        return;
    }

    try {
        showLoading(elements.catalogueResults);
        const data = await API.searchCatalogue(query, 20);
        state.catalogue = data.items || data || [];
        displayCatalogue(state.catalogue);
    } catch (error) {
        showError(elements.catalogueResults, 'Search failed');
        console.error(error);
    }
}

/**
 * Clear search and reload full catalogue
 */
function clearSearch() {
    elements.searchInput.value = '';
    loadCatalogue();
}

/**
 * Display catalogue items
 */
function displayCatalogue(items) {
    if (!items || items.length === 0) {
        elements.catalogueResults.innerHTML = '<div class="loading">No products found</div>';
        return;
    }

    elements.catalogueResults.innerHTML = items
        .map(item => createProductCard(item))
        .join('');

    // Add event listeners to product cards
    document.querySelectorAll('.product-card').forEach((card, index) => {
        const item = items[index];
        card.addEventListener('click', () => toggleItemSelection(item));
    });

    // Highlight selected items
    updateProductCardStates();
}

/**
 * Create a product card HTML
 */
function createProductCard(item) {
    const isSelected = state.selectedItems.some(i => i.id === item.id);
    return `
        <div class="product-card ${isSelected ? 'selected' : ''}">
            <div class="product-id">${item.id}</div>
            <div class="product-name">${item.name || 'Unknown'}</div>
            <div class="product-location">📍 ${item.location || 'N/A'}</div>
            <div class="product-qty">${item.quantity || 0}</div>
            <div class="product-actions">
                <button class="btn btn-primary" onclick="event.stopPropagation()">Add</button>
            </div>
        </div>
    `;
}

/**
 * Toggle product selection
 */
function toggleItemSelection(item) {
    const index = state.selectedItems.findIndex(i => i.id === item.id);
    if (index >= 0) {
        state.selectedItems.splice(index, 1);
    } else {
        state.selectedItems.push(item);
    }
    updateProductCardStates();
    updateOrderDisplay();
}

/**
 * Update visual state of product cards
 */
function updateProductCardStates() {
    document.querySelectorAll('.product-card').forEach((card, index) => {
        const item = state.catalogue[index];
        const isSelected = state.selectedItems.some(i => i.id === item.id);
        if (isSelected) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    });
}

/**
 * Load a demo order
 */
async function loadDemoOrder() {
    try {
        elements.demoBtn.disabled = true;
        elements.demoBtn.textContent = '⏳ Loading...';

        const data = await API.getDemoOrder();
        state.selectedItems = data.items || [];
        updateOrderDisplay();
        displayResponseData(data);

        // Update visualizer with demo data
        if (visualizer) {
            visualizer.update(data);
        }

        // Update stats
        if (data.total_distance !== undefined) {
            elements.statsDistance.textContent = data.total_distance.toFixed(2) + ' units';
        }
    } catch (error) {
        alert('Failed to load demo order');
        console.error(error);
    } finally {
        elements.demoBtn.disabled = false;
        elements.demoBtn.textContent = '📊 Load Demo Order';
    }
}

/**
 * Update order display
 */
function updateOrderDisplay() {
    // Update order list
    if (state.selectedItems.length === 0) {
        elements.orderList.innerHTML = '<p class="empty-state">No items selected</p>';
        elements.orderSummary.innerHTML = '<p class="empty-state">Select items to see summary</p>';
        return;
    }

    elements.orderList.innerHTML = state.selectedItems
        .map(item => `
            <div class="order-item">
                <div class="order-item-info">
                    <div class="order-item-id">${item.id}</div>
                    <div class="order-item-name">${item.name || 'Unknown'}</div>
                    <div class="order-item-loc">${item.location || 'N/A'}</div>
                </div>
                <button class="btn btn-secondary" onclick="removeItem('${item.id}')">Remove</button>
            </div>
        `)
        .join('');

    // Update summary
    elements.orderSummary.innerHTML = `
        <div class="summary-item">
            <span class="summary-label">Total Items:</span>
            <span class="summary-value">${state.selectedItems.length}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Locations:</span>
            <span class="summary-value">${new Set(state.selectedItems.map(i => i.location)).size}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Catalogue:</span>
            <span class="summary-value">${state.selectedItems[0]?.name?.split(' ')[0] || 'Mixed'}</span>
        </div>
    `;

    // Update product card states
    updateProductCardStates();
}

/**
 * Remove item from selection
 */
function removeItem(itemId) {
    state.selectedItems = state.selectedItems.filter(i => i.id !== itemId);
    updateOrderDisplay();
}

/**
 * Run order simulation
 */
async function runSimulation() {
    if (state.selectedItems.length === 0) {
        alert('Please select items first');
        return;
    }

    try {
        elements.simulateBtn.disabled = true;
        elements.simulateBtn.textContent = '⏳ Simulating...';

        const itemIds = state.selectedItems.map(i => i.id);
        const data = await API.simulateOrder(itemIds);
        state.currentSimulation = data;

        // Display response
        displayResponseData(data);

        // Update visualizer
        if (visualizer) {
            visualizer.update(data);
        }

        // Update stats
        updateSimulationStats(data);

        // Update pathfinding details
        updatePathfindingDetails(data);
    } catch (error) {
        alert('Simulation failed');
        console.error(error);
    } finally {
        elements.simulateBtn.disabled = false;
        elements.simulateBtn.textContent = '▶ Simulate Order';
    }
}

/**
 * Update simulation statistics
 */
function updateSimulationStats(data) {
    if (data.total_distance !== undefined) {
        elements.statsDistance.textContent = data.total_distance.toFixed(2) + ' units';
    }
    if (data.items) {
        elements.statsItems.textContent = data.items.length;
    }
    if (data.path) {
        elements.statsWaypoints.textContent = data.path.length;
    }
}

/**
 * Update pathfinding details
 */
function updatePathfindingDetails(data) {
    let html = '<div>';
    
    if (data.start_position) {
        html += `<div class="stat"><span class="label">Start:</span><span class="value">${data.start_position}</span></div>`;
    }
    
    if (data.end_position) {
        html += `<div class="stat"><span class="label">End:</span><span class="value">${data.end_position}</span></div>`;
    }

    if (data.algorithm) {
        html += `<div class="stat"><span class="label">Algorithm:</span><span class="value">${data.algorithm}</span></div>`;
    }

    if (data.total_distance !== undefined) {
        html += `<div class="stat"><span class="label">Distance:</span><span class="value">${data.total_distance.toFixed(2)}</span></div>`;
    }

    if (data.execution_time !== undefined) {
        html += `<div class="stat"><span class="label">Time:</span><span class="value">${data.execution_time.toFixed(3)}s</span></div>`;
    }

    html += '</div>';
    elements.pathfindingDetails.innerHTML = html;
}

/**
 * Clear the order
 */
function clearOrder() {
    state.selectedItems = [];
    state.currentSimulation = null;
    updateOrderDisplay();
    if (visualizer) {
        visualizer.clear();
    }
    elements.statsDistance.textContent = '-';
    elements.statsItems.textContent = '-';
    elements.statsWaypoints.textContent = '-';
    elements.pathfindingDetails.innerHTML = '<p class="empty-state">Run simulation to see details</p>';
    elements.responseData.textContent = 'Ready for simulation...';
}

/**
 * Display response data
 */
function displayResponseData(data) {
    elements.responseData.textContent = formatJSON(data, 2);
}

/**
 * Show loading state
 */
function showLoading(element) {
    element.innerHTML = '<div class="loading"><span class="spinner">⟳</span> Loading...</div>';
}

/**
 * Show error state
 */
function showError(element, message) {
    element.innerHTML = `<div class="loading" style="color: var(--danger);">❌ ${message}</div>`;
}

/**
 * Initialize app when DOM is ready
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
