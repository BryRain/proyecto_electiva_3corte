/* Authentication Functions */

function toggleAuthForm() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    if (loginForm.classList.contains('active')) {
        loginForm.classList.remove('active');
        registerForm.classList.add('active');
    } else {
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
    }
}

function initAuthEvents() {
    // Show auth section
    document.getElementById('auth-section').classList.remove('hidden');
    
    // Show login form by default
    document.getElementById('login-form').classList.add('active');

    // Login form handler
    document.getElementById('login-form').querySelector('form').addEventListener('submit', handleLogin);

    // Register form handler
    document.getElementById('register-form').querySelector('form').addEventListener('submit', handleRegister);
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');

    try {
        errorDiv.classList.remove('show');
        const result = await apiClient.login(email, password);
        
        apiClient.setToken(result.access_token);
        localStorage.setItem('user', JSON.stringify(result.user));
        
        showApp();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('show');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('register-email').value;
    const username = document.getElementById('register-username').value;
    const fullname = document.getElementById('register-fullname').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;
    const errorDiv = document.getElementById('register-error');

    try {
        errorDiv.classList.remove('show');
        
        if (password !== confirm) {
            throw new Error('Las contraseñas no coinciden');
        }

        if (password.length < 6) {
            throw new Error('La contraseña debe tener al menos 6 caracteres');
        }

        const result = await apiClient.register(email, username, password, fullname);
        
        alert('Registro exitoso. Por favor inicia sesión.');
        document.getElementById('login-email').value = email;
        toggleAuthForm();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('show');
    }
}

function showApp() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('app-section').classList.remove('hidden');
    
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    document.getElementById('user-greeting').textContent = `Hola, ${user.username || 'Usuario'}`;
    
    // Initialize app components
    initAppEvents();
    loadInitialData();
}

function logout() {
    if (confirm('¿Seguro que deseas cerrar sesión?')) {
        apiClient.clearToken();
        localStorage.removeItem('user');
        
        document.getElementById('app-section').classList.add('hidden');
        document.getElementById('auth-section').classList.remove('hidden');
        
        // Reset forms
        document.getElementById('login-form').reset();
        document.getElementById('register-form').reset();
        document.getElementById('login-form').classList.add('active');
        document.getElementById('register-form').classList.remove('active');
    }
}

// Check if already logged in
window.addEventListener('load', async () => {
    const token = localStorage.getItem('auth_token');
    
    if (token) {
        try {
            apiClient.setToken(token);
            await apiClient.getCurrentUser();
            showApp();
        } catch (error) {
            localStorage.removeItem('auth_token');
            initAuthEvents();
        }
    } else {
        initAuthEvents();
    }
});
