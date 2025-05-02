/**
 * @jest-environment jsdom
 */

const { toggleDarkMode } = require('./dark-mode');

describe('toggleDarkMode', () => {
  let body, icon;

  beforeEach(() => {
    // Simulate the required DOM structure
    document.body.innerHTML = `
      <div class="dark-mode-toggle">
        <i class="fa fa-moon"></i>
      </div>
    `;
    body = document.body;
    icon = document.querySelector('.dark-mode-toggle i');

    localStorage.clear();
  });

  test('enables dark mode and updates icon and localStorage', () => {
    toggleDarkMode();

    expect(body.classList.contains('dark-mode')).toBe(true);
    expect(icon.classList.contains('fa-sun')).toBe(true);
    expect(icon.classList.contains('fa-moon')).toBe(false);
    expect(localStorage.getItem('darkMode')).toBe('enabled');
  });

  test('disables dark mode and updates icon and localStorage', () => {
    // Set initial state to dark mode enabled
    body.classList.add('dark-mode');
    icon.classList.remove('fa-moon');
    icon.classList.add('fa-sun');
    localStorage.setItem('darkMode', 'enabled');

    toggleDarkMode();

    expect(body.classList.contains('dark-mode')).toBe(false);
    expect(icon.classList.contains('fa-moon')).toBe(true);
    expect(icon.classList.contains('fa-sun')).toBe(false);
    expect(localStorage.getItem('darkMode')).toBe('disabled');
  });
});
