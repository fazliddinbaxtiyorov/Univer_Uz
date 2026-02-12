/* ===================================
   UniBase - Theme Management
   Dark mode toggle functionality
   =================================== */

// Get saved theme or default to light
function getCurrentTheme() {
    return localStorage.getItem('unibase_theme') || 'light';
}

// Set theme
function setTheme(theme) {
    localStorage.setItem('unibase_theme', theme);
    applyTheme(theme);
}

// Apply theme to document
function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }

    // Update toggle button icon
    updateThemeToggleIcon(theme);
}

// Update theme toggle icon
function updateThemeToggleIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        if (theme === 'dark') {
            themeToggle.innerHTML = '☀️';
            themeToggle.title = 'Switch to light mode';
        } else {
            themeToggle.innerHTML = '🌙';
            themeToggle.title = 'Switch to dark mode';
        }
    }
}

// Toggle theme
function toggleTheme() {
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function () {
    const currentTheme = getCurrentTheme();
    applyTheme(currentTheme);

    // Theme toggle button event
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
});
