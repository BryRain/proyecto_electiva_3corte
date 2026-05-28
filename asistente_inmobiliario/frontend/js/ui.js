/* UI Helper Functions */

const PROPERTY_TYPE_LABELS = {
    apartment: 'Apartamento',
    house:     'Casa',
    office:    'Oficina',
    commercial: 'Comercial'
};

function initTabNavigation() {
    const navItems   = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const topbarTitle = document.getElementById('topbar-title');
    const sidebar    = document.getElementById('sidebar');

    const tabTitles = {
        search:     'Búsqueda IA',
        properties: 'Propiedades',
        favorites:  'Favoritos',
        agents:     'Agentes IA',
        documents:  'Documentos'
    };

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(n => n.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));

            item.classList.add('active');
            const tabName = item.getAttribute('data-tab');
            const tabEl = document.getElementById(`${tabName}-tab`);
            if (tabEl) {
                tabEl.classList.add('active');
                if (topbarTitle) topbarTitle.textContent = tabTitles[tabName] || '';

                if (tabName === 'properties') loadProperties();
                else if (tabName === 'favorites') loadFavorites();
                else if (tabName === 'agents') loadAgents();
            }

            // Close sidebar on mobile after navigation
            if (window.innerWidth <= 1024) {
                sidebar?.classList.remove('open');
            }
        });
    });

    // Sidebar toggle for mobile
    const toggle = document.getElementById('sidebar-toggle');
    toggle?.addEventListener('click', () => sidebar?.classList.toggle('open'));

    // Close sidebar clicking outside
    document.addEventListener('click', e => {
        if (window.innerWidth <= 1024 &&
            sidebar?.classList.contains('open') &&
            !sidebar.contains(e.target) &&
            e.target !== toggle) {
            sidebar.classList.remove('open');
        }
    });
}

function createPropertyCard(property) {
    const card = document.createElement('div');
    card.className = 'property-card';

    const typeLabel = PROPERTY_TYPE_LABELS[property.property_type] || property.property_type || '';

    card.innerHTML = `
        <div class="property-image">
            <i data-lucide="building-2"></i>
            ${typeLabel ? `<span class="property-type-badge">${typeLabel}</span>` : ''}
        </div>
        <div class="property-content">
            <div class="property-price">$${Number(property.price).toLocaleString('es-CO')}</div>
            <div class="property-address">
                <i data-lucide="map-pin"></i>
                ${property.address}
            </div>
            <div class="property-city">${property.city}${property.state ? ', ' + property.state : ''}</div>

            <div class="property-details">
                <div class="property-detail">
                    <i data-lucide="bed"></i>
                    <strong>${property.bedrooms ?? '-'}</strong>
                    <span>Hab.</span>
                </div>
                <div class="property-detail">
                    <i data-lucide="droplets"></i>
                    <strong>${property.bathrooms ?? '-'}</strong>
                    <span>Baños</span>
                </div>
                <div class="property-detail">
                    <i data-lucide="maximize-2"></i>
                    <strong>${property.area_sqm ?? '-'}</strong>
                    <span>m²</span>
                </div>
            </div>

            <div class="property-actions">
                <button class="btn btn-primary view-btn" data-id="${property.id}">
                    <i data-lucide="eye"></i>
                    Ver detalles
                </button>
                <button class="btn btn-ghost favorite-btn" data-id="${property.id}">
                    <i data-lucide="heart"></i>
                    Guardar
                </button>
            </div>
        </div>
    `;

    card.querySelector('.view-btn').addEventListener('click', () => showPropertyDetails(property));
    card.querySelector('.favorite-btn').addEventListener('click', () => toggleFavorite(property.id));

    // Re-render Lucide icons inside the new card
    lucide.createIcons({ nodes: [card] });

    return card;
}

function showPropertyDetails(property) {
    const modal    = document.getElementById('property-modal');
    const modalBody = document.getElementById('modal-body');
    const typeLabel = PROPERTY_TYPE_LABELS[property.property_type] || property.property_type || 'N/A';
    const amenities = Array.isArray(property.amenities)
        ? property.amenities
        : (property.amenities ? JSON.parse(property.amenities) : []);

    modalBody.innerHTML = `
        <h2>${property.address}</h2>
        <p><strong>Ubicación:</strong> ${property.city}${property.state ? ', ' + property.state : ''}${property.country ? ', ' + property.country : ''}</p>
        <p><strong>Precio:</strong> $${Number(property.price).toLocaleString('es-CO')}</p>
        <p><strong>Tipo:</strong> ${typeLabel}</p>
        <p><strong>Disponible:</strong> ${property.available ? 'Sí' : 'No'}</p>

        <h3>Detalles</h3>
        <ul>
            ${property.bedrooms != null ? `<li>Habitaciones: ${property.bedrooms}</li>` : ''}
            ${property.bathrooms != null ? `<li>Baños: ${property.bathrooms}</li>` : ''}
            ${property.area_sqm != null ? `<li>Área: ${property.area_sqm} m²</li>` : ''}
        </ul>

        ${property.description ? `<p><strong>Descripción:</strong><br>${property.description}</p>` : ''}

        ${amenities.length ? `
            <h3>Amenidades</h3>
            <p>${amenities.join(', ')}</p>
        ` : ''}

        <button class="btn btn-primary" onclick="toggleFavorite(${property.id})">
            <i data-lucide="heart"></i>
            Añadir a favoritos
        </button>
    `;

    lucide.createIcons({ nodes: [modalBody] });

    modal.classList.remove('hidden');
    modal.classList.add('show');
}

function toggleFavorite(propertyId) {
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
    const el = document.getElementById(elementId);
    if (!el) return;
    show ? el.classList.remove('hidden') : el.classList.add('hidden');
}

function showMessage(elementId, message, isError = false) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.classList.remove('hidden');
    el.classList.toggle('error', isError);

    if (!isError) {
        setTimeout(() => el.classList.add('hidden'), 3000);
    }
}

function createRAGResultItem(result) {
    const item = document.createElement('div');
    item.className = 'rag-item';
    const pct = result.similarity != null ? (result.similarity * 100).toFixed(0) : null;
    item.innerHTML = `
        <strong>
            <i data-lucide="file-text"></i>
            ${result.metadata?.filename || 'Documento'}
        </strong>
        <p>${result.content.substring(0, 200)}...</p>
        ${pct ? `<span class="relevance">Relevancia: ${pct}%</span>` : ''}
    `;
    lucide.createIcons({ nodes: [item] });
    return item;
}

// Modal close
document.addEventListener('click', e => {
    const closeBtn = e.target.closest('.modal-close, .btn-close');
    if (closeBtn) {
        const modal = document.getElementById('property-modal');
        modal?.classList.add('hidden');
        modal?.classList.remove('show');
    }

    const backdrop = e.target.closest('.modal-backdrop');
    if (backdrop) {
        const modal = backdrop.closest('.modal');
        modal?.classList.add('hidden');
        modal?.classList.remove('show');
    }
});

// Logout
document.getElementById('logout-btn')?.addEventListener('click', logout);

// Init Lucide after DOM load
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
});
