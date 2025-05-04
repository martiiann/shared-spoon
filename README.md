# Shared Spoon

**Shared Spoon** is a full-stack recipe sharing platform built with Django. It allows users to create accounts, post recipes, save favorites, search by ingredients, and interact with a dynamic and visually appealing interface. The site features a responsive design with dark mode support, AJAX-powered ingredient search, and user avatars.

Live Site: [https://shared-spoon-f2d629a69afc.herokuapp.com](https://shared-spoon-f2d629a69afc.herokuapp.com)  
Repository: [https://github.com/martiiann/shared-spoon](https://github.com/martiiann/shared-spoon)

---
## 📱 Responsive Overview

Below is how the site appears on different screen sizes:

| Mobile View | Tablet View | Desktop View |
|-------------|-------------|--------------|
| ![Mobile](README_IMAGES/mobile.png) | ![Tablet](README_IMAGES/tablet.png) | ![Desktop](README_IMAGES/desktop.png) |

---

## 🧭 Page Overviews

### 🏠 Home Page
- Displays a welcome message and search bar.
- Highlights latest recipes.
- Accessible to guests and logged-in users.

![Home](README_IMAGES/home.png)

---

### 👤 My Profile
- Users can upload avatars, edit profile details, and view a summary of activity.
- Shows all their submitted recipes.

![Profile](README_IMAGES/profile.png)

---

### ➕ Add Recipe
- Form to add a recipe with title, description, ingredients, quantities, and image.
- Select2 search input for ingredients.
- Dynamic formset to add/remove ingredients.
- Fully styled for dark/light mode.

![Add Recipe](README_IMAGES/add_recipe.png)

---

### ❤️ My Favorites
- Displays a grid of all favorited recipes.
- Includes recipe previews and ability to unfavorite.

![Favorites](README_IMAGES/favorites.png)

---

### 📓 My Recipes
- Displays a user’s own posted recipes.
- Includes edit/delete buttons if authenticated.

![My Recipes](README_IMAGES/my_recipes.png)

---

## Features

### Core Functionality

- **User Authentication**: Register, log in, log out.
- **Profile Management**: Upload avatars, edit bios.
- **Recipe CRUD**: Create, read, update, delete recipes.
- **AJAX Ingredient Search**: Dynamic Select2-powered search for ingredients.
- **Favorites System**: Users can favorite/unfavorite recipes.
- **Recipe Filtering**: Filter by ingredient or category.
- **Responsive Layout**: Fully optimized for mobile, tablet, and desktop.
- **Dark Mode**: Toggle dark/light mode for better accessibility.

---

## First-Time Visitor Goals

- Understand what the platform does upon landing.
- Explore recent and popular recipes.
- View single recipe details without account.
- Use search to quickly find relevant dishes.
- Easily register an account to contribute recipes.
- **Screenshot placeholder:** `screenshots/first-time-home.png`

---

## Returning Visitor Goals

- Log in and access saved (favorite) recipes.
- Add or manage personal recipes.
- Update profile with avatar and bio.
- Search by ingredients and categories.

---

## Functionality Overview

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Add Recipe                    | Title, category, image, instructions, and ingredients using formsets        |
| Ingredient Search             | AJAX-powered with Select2, results dynamically returned                      |
| Save Favorite                 | One-click save/unsave to personal list                                      |
| Dark Mode Toggle              | Retains preference via `localStorage`                                       |
| Profile Page                  | User recipes, avatar, bio                                                   |
| Admin Dashboard               | Available to superusers for moderation                                      |

---

## Design

- **Font**: 'Quicksand' via Google Fonts.
- **Color Theme**: Earthy tones with Bootstrap support.
- **Dark Mode**: Uses `body.dark-mode` class to switch palette.
- **Buttons & Cards**: Styled with consistent Bootstrap 5 and custom shadows.
- **CSS**: Clean, commented, organized by sections (base, dark mode, recipe cards, forms).

---

## Validator Testing

### HTML
- Validated with [W3C HTML Validator](https://validator.w3.org/)
- **Screenshot placeholder**: `screenshots/html-validation.png`

### CSS
- Validated with [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
- **Screenshot placeholder**: `screenshots/css-validation.png`

### JavaScript
- Checked with [JSHint](https://jshint.com/)
- No critical warnings or errors.
- **Screenshot placeholder**: `screenshots/js-validation.png`

### Python
- Validated using [Code Institute Python Linter](https://pep8ci.herokuapp.com/)
- **Screenshot placeholder**: `screenshots/python-validation.png`

---

## Manual Testing Table

| Feature                        | Test Description                            | Expected Outcome          | Status     |
|-------------------------------|---------------------------------------------|---------------------------|------------|
| Register User                 | Fill and submit form                        | New user created          | Pass       |
| Add Recipe                    | Submit form with ingredients                | Recipe saved              | Pass       |
| Favorite Toggle               | Click heart icon                            | Recipe added/removed      | Pass       |
| Ingredient Search             | Type “sugar” in ingredient field            | Relevant results appear   | Pass       |
| Dark Mode                     | Toggle switch                               | Colors inverted           | Pass       |
| Admin Login                   | Login as superuser                          | Dashboard access          | Pass       |
| Update Profile                | Change avatar and bio                       | Profile updated           | Pass       |
| Mobile Layout                 | Open site on phone                          | Layout responsive         | Pass       |

### Manual Test Evidence

- **Screenshot placeholder**: `screenshots/manual-add.png`
- **Screenshot placeholder**: `screenshots/manual-search.png`
- **Screenshot placeholder**: `screenshots/manual-favorite.png`

---

## Performance Testing

Tested with Google Lighthouse in Chrome.

| Category        | Score |
|-----------------|-------|
| Performance     | 96    |
| Accessibility   | 88    |
| Best Practices  | 93    |
| SEO             | 91    |

- **Screenshot placeholder**: `screenshots/lighthouse.png`

---

## Future Features

- User comments on recipes
- Recipe rating system
- Upload multiple recipe images
- Ingredient stock tracker (inventory style)
- Shareable recipe links with previews

---

## Deployment

The site is hosted on Heroku: [Shared Spoon](https://shared-spoon-f2d629a69afc.herokuapp.com)

---

## Acknowledgments

- [Code Institute](https://codeinstitute.net/)
- Bootstrap, jQuery, Select2, Font Awesome
- [Unsplash](https://unsplash.com/) and [Pexels](https://pexels.com) for sample images
- Heroku for hosting

---