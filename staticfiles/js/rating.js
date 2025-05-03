/* global Swal */

async function handleRatingClick(event) {
    if (!event.target.classList.contains('submit-rating-btn')) return;
  
    const button = event.target;
    const container = button.closest('.rating-container');
    const recipeId = container.dataset.recipeId;
    const form = button.closest('form');
    const feedbackDiv = container.querySelector('.rating-feedback');
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
  
    if (button.innerText.includes('Edit')) {
      container.querySelector('.edit-rating-select').style.display = 'flex';
      button.style.display = 'none';
      return;
    }
  
    const rating = form.querySelector('select[name="rating"]').value;
    if (!rating) {
      feedbackDiv.innerHTML =
        '<div class="alert alert-warning p-2">Please select a rating first!';
      return;
    }
  
    button.disabled = true;
    const oldHtml = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
  
    try {
      const resp = await fetch(`/rate-recipe/${recipeId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: `rating=${rating}`
      });
  
      const data = await resp.json();
      if (!resp.ok || !data.success) throw new Error(data.error || 'Submission failed');
  
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: `You rated this ${rating} ⭐`,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true
      });
  
      container.querySelector('.edit-rating-select').style.display = 'none';
      button.style.display = 'inline-block';
      button.textContent = 'Edit your rating';
  
      const disp = document.getElementById(`rating-display-${recipeId}`);
      if (disp && typeof data.avg_rating === 'number') {
        disp.textContent = `${data.avg_rating.toFixed(1)} ⭐`;
      }
    } catch (err) {
      feedbackDiv.innerHTML = `<div class="alert alert-danger p-2">Error: ${err.message}</div>`;
    } finally {
      button.disabled = false;
      button.innerHTML = oldHtml;
    }
  }
  
  async function handleFavoriteSubmit(event) {
    if (!event.target.classList.contains('toggle-favorite-form')) return;
  
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('button[type="submit"]');
    const csrf = form.querySelector('[name=csrfmiddlewaretoken]').value;
  
    try {
      const resp = await fetch(form.action, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrf
        }
      });
  
      const data = await resp.json();
      if (!data.success) throw new Error('Toggle failed');
  
      if (data.favorited) {
        btn.classList.replace('btn-outline-danger', 'btn-danger');
        btn.innerHTML = '<i class="bi bi-heart-fill text-white me-1"></i>Unsave';
      } else {
        btn.classList.replace('btn-danger', 'btn-outline-danger');
        btn.innerHTML = '<i class="bi bi-heart me-1"></i>Save';
      }
  
      const card = form.closest('.recipe-card');
      const counter = card.querySelector('.saved-count');
      if (counter) {
        const n = data.liked_by_count;
        counter.textContent = `❤️ ${n} user${n === 1 ? '' : 's'}`;
      }
  
      Swal.fire({
        position: 'center',
        icon: data.favorited ? 'success' : 'info',
        title: data.favorited
          ? 'Recipe Added to Favorites!'
          : 'Recipe Removed from Favorites!',
        text: data.favorited
          ? 'Great choice! This recipe is now safely stored in your favorites list for easy access anytime.'
          : 'No worries! This recipe has been taken off your favorites list—you can always save it again later.',
        showConfirmButton: true,
        confirmButtonText: 'OK',
        timer: 3000,
        timerProgressBar: true
      });
    } catch (err) {
      console.error(err);
      Swal.fire({
        position: 'center',
        icon: 'error',
        title: 'Oops!',
        text: 'Could not update favorite. Please try again.',
        showConfirmButton: true
      });
    }
  }
  
  // Export the functions so you can test them
  module.exports = {
    handleRatingClick,
    handleFavoriteSubmit
  };
  