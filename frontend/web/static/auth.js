document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const logoutBtn = document.getElementById('logout-btn');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
        // Mostrar bienvenida
        const username = sessionStorage.getItem('username');
        if(username) {
            document.getElementById('welcome-user').textContent = `Bienvenido, ${username}`;
        } else {
            // Si no hay sesión, volver al login
            window.location.href = '/';
        }
    }
});

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch('/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
        const data = await response.json();
        // Guardamos info del usuario en sessionStorage
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('email', data.email); // Asumimos que el login devuelve el email
        alert('Login exitoso!');
        window.location.href = '/shop';
    } else {
        alert('Error: Usuario o contraseña incorrectos.');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch('/api/users/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, username, password })
    });

    if (response.status === 201) {
        alert('Registro exitoso! Por favor, inicia sesión.');
        window.location.href = '/';
    } else {
        const data = await response.json();
        alert(`Error en el registro: ${data.message}`);
    }
}

function handleLogout() {
    sessionStorage.clear();
    alert('Sesión cerrada.');
    window.location.href = '/';
}
