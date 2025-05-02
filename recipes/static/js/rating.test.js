/**
 * @jest-environment jsdom
 */

const { handleRatingClick, handleFavoriteSubmit } = require('./rating');

describe('Rating submission', () => {
  let button, form, container, feedback, csrf, display;

  beforeEach(() => {
    document.body.innerHTML = `
      <div class="rating-container" data-recipe-id="42">
        <form>
          <input type="hidden" name="csrfmiddlewaretoken" value="csrf-token" />
          <select name="rating">
            <option value="">Select</option>
            <option value="5" selected>5</option>
          </select>
          <button class="submit-rating-btn">Submit</button>
        </form>
        <div class="edit-rating-select" style="display: none;"></div>
        <div class="rating-feedback"></div>
      </div>
      <div id="rating-display-42"></div>
    `;

    container = document.querySelector('.rating-container');
    form = container.querySelector('form');
    button = container.querySelector('.submit-rating-btn');
    feedback = container.querySelector('.rating-feedback');
    csrf = form.querySelector('[name=csrfmiddlewaretoken]');
    display = document.getElementById('rating-display-42');

    // Mock innerText for jsdom compatibility
    Object.defineProperty(button, 'innerText', {
      get: () => 'Submit',
      configurable: true,
    });

    global.Swal = { fire: jest.fn() };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true, avg_rating: 4.5 }),
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('submits rating with correct data', async () => {
    const event = new MouseEvent('click', { bubbles: true });
    Object.defineProperty(event, 'target', { value: button });

    await handleRatingClick(event);

    expect(fetch).toHaveBeenCalledWith('/rate-recipe/42/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': 'csrf-token',
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: 'rating=5',
    });

    expect(Swal.fire).toHaveBeenCalledWith(
      expect.objectContaining({
        icon: 'success',
        title: 'You rated this 5 ⭐',
      })
    );

    expect(display.textContent).toBe('4.5 ⭐');
  });

  test('shows warning if no rating is selected', async () => {
    form.querySelector('select[name="rating"]').value = '';
    const event = new MouseEvent('click', { bubbles: true });
    Object.defineProperty(event, 'target', { value: button });

    await handleRatingClick(event);

    expect(feedback.innerHTML).toMatch(/Please select a rating/);
    expect(fetch).not.toHaveBeenCalled();
  });
});

describe('Favorite toggle', () => {
  let form, button, counter;

  beforeEach(() => {
    document.body.innerHTML = `
      <div class="recipe-card">
        <form class="toggle-favorite-form" action="/toggle-fav/42/">
          <input type="hidden" name="csrfmiddlewaretoken" value="csrf-token" />
          <button type="submit" class="btn btn-outline-danger">
            <i class="bi bi-heart me-1"></i>Save
          </button>
          <div class="saved-count">❤️ 0 users</div>
        </form>
      </div>
    `;

    form = document.querySelector('form');
    button = form.querySelector('button');
    counter = document.querySelector('.saved-count');

    global.Swal = { fire: jest.fn() };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({ success: true, favorited: true, liked_by_count: 3 }),
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('toggles favorite and updates UI', async () => {
    const event = new Event('submit', { bubbles: true });
    Object.defineProperty(event, 'target', { value: form });

    await handleFavoriteSubmit(event);

    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/toggle-fav/42/'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': 'csrf-token',
        'X-Requested-With': 'XMLHttpRequest',
      },
    });

    expect(button.classList.contains('btn-danger')).toBe(true);
    expect(button.innerHTML).toMatch(/Unsave/);
    expect(counter.textContent).toBe('❤️ 3 users');

    expect(Swal.fire).toHaveBeenCalledWith(
      expect.objectContaining({
        icon: 'success',
        title: 'Recipe Added to Favorites!',
      })
    );
  });
});
