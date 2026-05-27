/* UI Helper Functions */

function initTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked
            button.classList.add('active');
            const tabName = button.getAttribute('data-tab');
            const tabElement = document.getElementById(`${tabName}-tab`);
            if (tabElement) {
                tabElement.classList.add('active');
                
                // Load data based on tab
                if (tabName === 'properties') {
                    loadProperties();
                } else if (tabName === 'favorites') {
                    loadFavorites();
                } else if (tabName === 'agents') {
                    loadAgents();
                }
            }
        });
    });
}

function createPropertyCard(property) {
    const card = document.createElement('div');
    card.className = 'property-card';
    card.innerHTML = `
        <div class="property-image">
            🏠
        </div>
        <div class="property-content">
            <div class="property-price">$${property.price.toLocaleString()}</div>
            <div class="property-address">${property.address}</div>
            <div class="property-city">${property.city}, ${property.state}</div>
            
            <div class="property-details">
                <div class="property-detail">
                    <strong>${property.bedrooms || '-'}</strong>
                    <br>Hab.
                </div>
                <div class="property-detail">
                    <strong>${property.bathrooms || '-'}</strong>
                    <br>Baños
                </div>
                <div class="property-detail">
                    <strong>${property.area_sqm || '-'}</strong>
                    <br>m²
                </div>
            </div>
            
            <div class="property-actions">
                <button class="btn btn-primary view-btn" data-id="${property.id}">Ver Detalles</button>
                <button class="btn btn-secondary favorite-btn" data-id="${property.id}">❤️ Favorito</button>
            </div>
        </div>
    `;

    card.querySelector('.view-btn').addEventListener('click', () => showPropertyDetails(property));
    card.querySelector('.favorite-btn').addEventListener('click', () => toggleFavorite(property.id));

    return card;
}

function showPropertyDetails(property) {
    const modal = document.getElementById('property-modal');
    const modalBody = document.getElementById('modal-body');

    modalBody.innerHTML = `
        <h2>${property.address}</h2>
        <p><strong>Ubicación:</strong> ${property.city}, ${property.state}, ${property.country}</p>
        <p><strong>Precio:</strong> $${property.price.toLocaleString()}</p>
        <p><strong>Tipo:</strong> ${property.property_type || 'N/A'}</p>
        
        <h3>Detalles</h3>
        <ul>
            <li>Habitaciones: ${property.bedrooms || 'N/A'}</li>
            <li>Baños: ${property.bathrooms || 'N/A'}</li>
            <li>Área: ${property.area_sqm || 'N/A'} m²</li>
            <li>Disponible: ${property.available ? 'Sí' : 'No'}</li>
        </ul>
        
        ${property.description ? `<p><strong>Descripción:</strong><br>${property.description}</p>` : ''}
        
        ${property.amenities ? `
            <h3>Amenidades</h3>
            <p>${Array.isArray(property.amenities) ? property.amenities.join(', ') : property.amenities}</p>
        ` : ''}
        
        <button class="btn btn-primary" onclick="toggleFavorite(${property.id})">Añadir a Favoritos</button>
    `;

    modal.classList.remove('hidden');
    modal.classList.add('show');
}

function toggleFavorite(propertyId) {
    // Implementar en app.js
    addPropertyFavorite(propertyId);
}

function formatAgentResponse(agentName, response) {
    const card = document.createElement('div');
    card.className = 'agent-card';
    card.innerHTML = `
        <h5>${agentName}</h5>
        <p>${response}</p>
    `;
    return card;
}

function showLoading(elementId, show = true) {
    const element = document.getElementById(elementId);
    if (show) {
        element.classList.remove('hidden');
    } else {
        element.classList.add('hidden');
    }
}

function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.classList.remove('hidden');
    
    if (isError) {
        element.classList.add('error');
    } else {
        element.classList.remove('error');
    }
    
    if (!isError) {
        setTimeout(() => {
            element.classList.add('hidden');
        }, 3000);
    }
}

function createRAGResultItem(result) {
    const item = document.createElement('div');
    item.className = 'rag-item';
    item.innerHTML = `
        <strong>📄 ${result.metadata?.filename || 'Documento'}</strong>
        <p>${result.content.substring(0, 200)}...</p>
        <div class="relevance">Relevancia: ${(result.similarity * 100).toFixed(0)}%</div>
    `;
    return item;
}

// Modal close handlers
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-close')) {
        const modal = e.target.closest('.modal');
        modal.classList.add('hidden');
        modal.classList.remove('show');
    }
});

// Logout handler
document.getElementById('logout-btn')?.addEventListener('click', logout);
