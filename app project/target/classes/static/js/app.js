// Main application JavaScript
// Token management and navigation

const API_BASE_URL = 'http://localhost:8080/api';

// Token management
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
}

function getUsername() {
    return localStorage.getItem('username');
}

function setUsername(username) {
    localStorage.setItem('username', username);
}

// Check if user is logged in
function isLoggedIn() {
    return getToken() !== null;
}

// Update navigation based on login status
function updateNavigation() {
    const loginLink = document.getElementById('loginLink');
    const signupLink = document.getElementById('signupLink');
    const dashboardLink = document.getElementById('dashboardLink');
    const logoutLink = document.getElementById('logoutLink');

    if (isLoggedIn()) {
        if (loginLink) loginLink.style.display = 'none';
        if (signupLink) signupLink.style.display = 'none';
        if (dashboardLink) {
            dashboardLink.style.display = 'inline';
            dashboardLink.href = '/dashboard.html';
        }
        if (logoutLink) logoutLink.style.display = 'inline';
    } else {
        if (loginLink) loginLink.style.display = 'inline';
        if (signupLink) signupLink.style.display = 'inline';
        if (dashboardLink) dashboardLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'none';
    }
}

// Logout function
function logout() {
    removeToken();
    window.location.href = '/index.html';
}

// Initialize navigation on page load
document.addEventListener('DOMContentLoaded', function() {
    updateNavigation();

    // Add logout event listener
    const logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
});

