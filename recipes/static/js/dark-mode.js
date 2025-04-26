function toggleDarkMode() {
    const body = document.body;
    const icon = document.querySelector('.dark-mode-toggle i');

    // Toggle the dark mode class
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        // Switch icon and save preference
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        localStorage.setItem('darkMode', 'enabled');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        localStorage.setItem('darkMode', 'disabled');
    }
}

// Check dark mode status on page load
document.addEventListener('DOMContentLoaded', function () {
    const darkModeEnabled = localStorage.getItem('darkMode') === 'enabled';
    const prefersDarkScheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const body = document.body;
    const icon = document.querySelector('.dark-mode-toggle i');

    if (darkModeEnabled || (!localStorage.getItem('darkMode') && prefersDarkScheme)) {
        // Apply dark mode if enabled or preferred by system
        body.classList.add('dark-mode');
        if (icon) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
});
