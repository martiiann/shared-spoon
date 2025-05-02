/**
 * @jest-environment jsdom
 */

describe('ingredient search input', () => {
    let input;
  
    beforeEach(() => {
      // Set up the DOM structure with an input element
      document.body.innerHTML = `
        <input type="text" class="ingredient-search" />
      `;
      input = document.querySelector('.ingredient-search');
  
      // Mock document.cookie to provide CSRF token
      Object.defineProperty(document, 'cookie', {
        writable: true,
        value: 'csrftoken=testtoken',
      });
  
      // Mock global fetch
      global.fetch = jest.fn(() =>
        Promise.resolve({
          json: () => Promise.resolve({ results: ['salt', 'sugar'] }),
        })
      );
  
      // Require the script and manually trigger DOMContentLoaded
      jest.isolateModules(() => {
        require('./recipes'); // adjust if your filename is different
        document.dispatchEvent(new Event('DOMContentLoaded'));
      });
    });
  
    afterEach(() => {
      jest.clearAllMocks();
    });
  
    test('should not call fetch on short input', () => {
      input.value = 'a';
      input.dispatchEvent(new Event('input'));
  
      expect(fetch).not.toHaveBeenCalled();
    });
  
    test('should call fetch with correct params on valid input', async () => {
      input.value = 'su';
      input.dispatchEvent(new Event('input'));
  
      // Allow async fetch to resolve
      await new Promise(process.nextTick);
  
      expect(fetch).toHaveBeenCalledWith('/api/ingredients/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': 'testtoken',
        },
        body: 'q=su',
      });
    });
  });
  