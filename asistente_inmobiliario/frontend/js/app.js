/* Main Application Logic */

let currentPage = 1;
let currentFilters = {};

function initAppEvents() {
    initTabNavigation();
    
    // AI Search
    document.getElementById('ai-search-btn').addEventListener('click', handleAISearch);
    document.getElementById('ai-search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAISearch();
    });

    // Properties
    document.getElementById('apply-filters-btn').addEventListener('click', applyFilters);
    document.getElementById('clear-filters-btn').addEventListener('click', clearFilters);

    // Agents
    loadAgents();

    // Documents
    initDocumentUpload();
    document.getElementById('doc-search-btn').addEventListener('click', handleDocumentSearch);
}

async function loadInitialData() {
    try {
        await loadProperties();
        await loadFavorites();
    } catch (error) {
        console.error('Error loading initial data:', error);
    }
}

// ==================== AI SEARCH ====================

async function handleAISearch() {
    const query = document.getElementById('ai-search-input').value.trim();
    
    if (!query) {
        alert('Por favor escribe una búsqueda');
        return;
    }

    showLoading('search-loading', true);
    
    try {
        const result = await apiClient.aiSearch(query);
        displayAIResponse(result);
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        showLoading('search-loading', false);
    }
}

function displayAIResponse(result) {
    const responseDiv = document.getElementById('ai-response');
    const contentDiv = document.getElementById('ai-response-content');
    const agentsDiv = document.getElementById('agents-responses');
    const ragDiv = document.getElementById('rag-results');

    // Main synthesis - Solo mostrar la respuesta del coordinador
    const synthesis = result.ai_response?.agents_responses?.coordinator?.response || result.synthesis?.response || 'Análisis completado';
    contentDiv.innerHTML = `<p>${synthesis}</p>`;

    // Agents responses - Solo mostrar search y evaluator (más relevantes)
    agentsDiv.innerHTML = '';
    if (result.ai_response?.agents_responses) {
        const relevantAgents = ['search', 'evaluator'];
        relevantAgents.forEach(agentKey => {
            const agent = result.ai_response.agents_responses[agentKey];
            if (agent) {
                agentsDiv.appendChild(formatAgentResponse(agentKey, agent.response));
            }
        });
    }

    // RAG results
    ragDiv.innerHTML = '';
    if (result.rag_documents && result.rag_documents.length > 0) {
        result.rag_documents.forEach(doc => {
            ragDiv.appendChild(createRAGResultItem(doc));
        });
    } else {
        ragDiv.innerHTML = '<p>No se encontraron documentos relevantes</p>';
    }

    responseDiv.classList.remove('hidden');
}

// ==================== PROPERTIES ====================

async function loadProperties(page = 1) {
    try {
        currentPage = page;
        const result = await apiClient.getProperties({
            ...currentFilters,
            page,
            per_page: 12
        });

        displayProperties(result.properties);
        displayPagination(result.pages, page);
    } catch (error) {
        console.error('Error loading properties:', error);
        document.getElementById('properties-grid').innerHTML = 
            '<div class="no-results">Error cargando propiedades</div>';
    }
}

function displayProperties(properties) {
    const grid = document.getElementById('properties-grid');
    
    if (properties.length === 0) {
        grid.innerHTML = '<div class="no-results">No se encontraron propiedades</div>';
        return;
    }

    grid.innerHTML = '';
    properties.forEach(property => {
        grid.appendChild(createPropertyCard(property));
    });
}

function displayPagination(pages, currentPage) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    if (pages <= 1) return;

    // Previous
    if (currentPage > 1) {
        const prevBtn = document.createElement('button');
        prevBtn.textContent = '← Anterior';
        prevBtn.addEventListener('click', () => loadProperties(currentPage - 1));
        pagination.appendChild(prevBtn);
    }

    // Page numbers
    for (let i = 1; i <= pages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        if (i === currentPage) btn.classList.add('active');
        btn.addEventListener('click', () => loadProperties(i));
        pagination.appendChild(btn);
    }

    // Next
    if (currentPage < pages) {
        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Siguiente →';
        nextBtn.addEventListener('click', () => loadProperties(currentPage + 1));
        pagination.appendChild(nextBtn);
    }
}

function applyFilters() {
    currentFilters = {
        city: document.getElementById('filter-city').value,
        min_price: document.getElementById('filter-min-price').value,
        max_price: document.getElementById('filter-max-price').value,
        type: document.getElementById('filter-type').value,
        bedrooms: document.getElementById('filter-bedrooms').value
    };

    loadProperties(1);
}

function clearFilters() {
    currentFilters = {};
    document.getElementById('filter-city').value = '';
    document.getElementById('filter-min-price').value = '';
    document.getElementById('filter-max-price').value = '';
    document.getElementById('filter-type').value = '';
    document.getElementById('filter-bedrooms').value = '';
    
    loadProperties(1);
}

// ==================== FAVORITES ====================

async function loadFavorites() {
    try {
        const result = await apiClient.getFavorites();
        displayFavorites(result.favorites);
    } catch (error) {
        console.error('Error loading favorites:', error);
    }
}

function displayFavorites(favorites) {
    const grid = document.getElementById('favorites-grid');
    
    if (favorites.length === 0) {
        grid.innerHTML = '<div class="no-results">No hay favoritos aún</div>';
        return;
    }

    grid.innerHTML = '';
    favorites.forEach(property => {
        grid.appendChild(createPropertyCard(property));
    });
}

async function addPropertyFavorite(propertyId) {
    try {
        await apiClient.addFavorite(propertyId);
        alert('Añadido a favoritos');
        await loadFavorites();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== AGENTS ====================

async function loadAgents() {
    try {
        const result = await apiClient.getAgents();
        
        const agentsList = document.getElementById('agents-list');
        agentsList.innerHTML = '';
        
        result.agents.forEach(agent => {
            const card = document.createElement('div');
            card.className = 'agent-card';
            card.innerHTML = `
                <h5>${agent.name}</h5>
                <p>${agent.role}</p>
            `;
            agentsList.appendChild(card);
        });

        // Populate agent select
        const select = document.getElementById('agent-select');
        result.agents.forEach(agent => {
            const option = document.createElement('option');
            option.value = agent.name;
            option.textContent = agent.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading agents:', error);
    }
}

document.getElementById('execute-agent-btn')?.addEventListener('click', async () => {
    const agentName = document.getElementById('agent-select').value;
    const task = document.getElementById('agent-task').value;

    if (!agentName || !task) {
        alert('Selecciona un agente y escribe una tarea');
        return;
    }

    try {
        const result = await apiClient.executeAgent(agentName, task);
        
        const resultDiv = document.getElementById('agent-result');
        resultDiv.innerHTML = `
            <h4>${result.agent}</h4>
            <p>${result.result.response}</p>
        `;
        resultDiv.classList.remove('hidden');
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// ==================== DOCUMENTS ====================

function initDocumentUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');

    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.background = '#f0f4ff';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.background = '#f9f9f9';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.background = '#f9f9f9';
        fileInput.files = e.dataTransfer.files;
    });

    uploadBtn.addEventListener('click', handleDocumentUpload);
}

async function handleDocumentUpload() {
    const fileInput = document.getElementById('file-input');
    const files = fileInput.files;

    if (files.length === 0) {
        alert('Selecciona archivos primero');
        return;
    }

    const statusDiv = document.getElementById('upload-status');
    
    try {
        for (let file of files) {
            statusDiv.innerHTML = `Subiendo ${file.name}...`;
            await apiClient.uploadDocument(file);
        }
        
        statusDiv.innerHTML = '✓ Documentos subidos exitosamente';
        fileInput.value = '';
    } catch (error) {
        statusDiv.innerHTML = `✗ Error: ${error.message}`;
    }
}

async function handleDocumentSearch() {
    const query = document.getElementById('doc-search-input').value.trim();
    
    if (!query) {
        alert('Escribe una búsqueda');
        return;
    }

    try {
        const result = await apiClient.ragSearch(query);
        
        const resultsDiv = document.getElementById('doc-search-results');
        resultsDiv.innerHTML = '';

        if (result.results.length === 0) {
            resultsDiv.innerHTML = '<p>No se encontraron resultados</p>';
            return;
        }

        result.results.forEach(doc => {
            resultsDiv.appendChild(createRAGResultItem(doc));
        });
    } catch (error) {
        alert('Error: ' + error.message);
    }
}
