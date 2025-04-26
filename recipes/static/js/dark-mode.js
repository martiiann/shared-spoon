function toggleDarkMode() {
    const body = document.body;
    const icon = document.querySelector('.dark-mode-toggle i');
  
    // Toggle the dark mode class on body
    body.classList.toggle('dark-mode');
  
    // Change icon based on the mode
    if (body.classList.contains('dark-mode')) {
      icon.classList.remove('fa-moon');
      icon.classList.add('fa-sun');
    } else {
      icon.classList.remove('fa-sun');
      icon.classList.add('fa-moon');
    }
  
    // Save the dark mode preference to localStorage
    if (window.localStorage) {
      localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
    }
  }
  
  // Load dark mode on page load based on localStorage or system preference
  document.addEventListener('DOMContentLoaded', function () {
    const darkModeEnabled = localStorage.getItem('darkMode') === 'true';
    const prefersDarkScheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const body = document.body;
    const icon = document.querySelector('.dark-mode-toggle i');
  
    // Apply dark mode if it was previously enabled or if system prefers dark mode
    if (darkModeEnabled) {
      body.classList.add('dark-mode');
      if (icon) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
      }
    } else if (prefersDarkScheme) {
      body.classList.add('dark-mode');
      if (icon) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
      }
    }
  });
  
  