function toggleDarkMode() {
    const body = document.body;
    const icon = document.querySelector('.dark-mode-toggle i');
  
    body.classList.toggle('dark-mode');
  
    // Change icon
    if (body.classList.contains('dark-mode')) {
      icon.classList.remove('fa-moon');
      icon.classList.add('fa-sun');
    } else {
      icon.classList.remove('fa-sun');
      icon.classList.add('fa-moon');
    }
  
    // Save preference to localStorage
    if (window.localStorage) {
      localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
    }
  }
  
  // Load dark mode on page load if previously enabled
  document.addEventListener('DOMContentLoaded', function () {
    const darkModeEnabled = localStorage.getItem('darkMode') === 'true';
    const body = document.body;
    const icon = document.querySelector('.dark-mode-toggle i');
  
    if (darkModeEnabled) {
      body.classList.add('dark-mode');
      if (icon) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
      }
    }
  });
  