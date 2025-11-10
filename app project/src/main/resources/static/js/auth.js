// Authentication JavaScript

// Login form handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('errorMessage');
        
        try {
            const response = await fetch('http://localhost:8080/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok && data.token) {
                setToken(data.token);
                setUsername(data.username);
                window.location.href = '/dashboard.html';
            } else {
                errorMessage.textContent = data.message || 'Login failed. Please try again.';
                errorMessage.style.display = 'block';
            }
        } catch (error) {
            errorMessage.textContent = 'An error occurred. Please try again.';
            errorMessage.style.display = 'block';
            console.error('Login error:', error);
        }
    });
}

// Signup form handler
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('signupUsername').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        const errorMessage = document.getElementById('errorMessage');
        
        try {
            const response = await fetch('http://localhost:8080/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (response.ok && data.token) {
                setToken(data.token);
                setUsername(data.username);
                window.location.href = '/dashboard.html';
            } else {
                errorMessage.textContent = data.message || 'Signup failed. Please try again.';
                errorMessage.style.display = 'block';
            }
        } catch (error) {
            errorMessage.textContent = 'An error occurred. Please try again.';
            errorMessage.style.display = 'block';
            console.error('Signup error:', error);
        }
    });
}

