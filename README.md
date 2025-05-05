# Shared Spoon 🍴

![Shared Spoon Preview](README_IMAGES/desktopoverviewhome.png)

**Shared Spoon** is a full-stack recipe web application where users can register, log in, add recipes, browse others’ creations, and mark their favorites. Built using Django and PostgreSQL, it features responsive design, dynamic ingredient search using Select2, user profiles with avatars, and dark mode toggle for a personalized experience.

🔗 [Live Site](https://shared-spoon-f2d629a69afc.herokuapp.com)  
💻 [GitHub Repository](https://github.com/martiiann/shared-spoon)

---

## 📚 Table of Contents

- [Responsive Overview](#-responsive-overview)
- [Page Overviews](#-page-overviews)
- [Wireframes](#-wireframes)
- [Features](#-features)
- [Functionality Overview](#-functionality-overview)
- [Manual Testing Table](#-manual-testing-table)
- [First-Time Visitor Goals](#-first-time-visitor-goals)
- [Returning Visitor Goals](#returning-visitor-goals)
- [Design](#design)
- [Validator Testing](#-validator-testing)
- [Performance](#-performance)
- [Devices Tested](#-devices-tested)
- [Future Features](#-future-features)
- [Deployment](#-deployment)
- [Debugging & Problem Solving](#-debugging--problem-solving)
- [Lessons Learned](#-lessons-learned)
- [Acknowledgments](#-acknowledgments)

---

## 📱 Responsive Overview

> **Note**: Mobile, tablet, and desktop views are tested manually and verified for responsiveness.

| Mobile View | Tablet View | Desktop View |
|-------------|-------------|--------------|
| ![Mobile](README_IMAGES/mobile.png) | ![Tablet](README_IMAGES/tablet.png) | ![Desktop](README_IMAGES/desktop.png) |

---

## 🧭 Page Overviews

### 🏠 Home Page
![Home](README_IMAGES/desktopoverviewhome.png)

### 👤 My Profile
![Profile](README_IMAGES/profileoverview.png)

### ➕ Add Recipe
![Add Recipe](README_IMAGES/addrecipeoverview.png)

### ❤️ My Favorites
![Favorites](README_IMAGES/favoriteoverview.png)

### 📓 My Recipes
![My Recipes](README_IMAGES/myrecipesoverview.png)

---

## 🧩 Wireframes

> All wireframes reflect desktop layout. Responsiveness is confirmed through manual testing.

### Home Page
![Wireframe - Home](README_IMAGES/homepagewireframe.png)

### Add Recipe
![Wireframe - Add Recipe](README_IMAGES/addrecipewireframe.png)

### My Recipes
![Wireframe - My Recipes](README_IMAGES/myrecipewireframe.png)

### Profile
![Wireframe - Profile](README_IMAGES/profilewireframe.png)

### Recipe Detail
![Wireframe - Recipe Detail](README_IMAGES/recipedetailwireframe.png)

---

## ✨ Features

- **User Authentication**: Register, login, and logout.
- **CRUD Recipes**: Add, update, delete recipes.
- **Favorites**: Users can save and manage favorites.
- **Profile Page**: Avatar upload, view own activity.
- **Searchable Ingredients**: AJAX-powered Select2 dropdown.
- **Dark Mode**: Toggle available for all users.
- **Responsive Design**: Mobile-first layout.
- **Pagination**: For recipe listings.

---

## 🧮 Functionality Overview

| Feature                        | Description                                                                |
|-------------------------------|-----------------------------------------------------------------------------|
| Add Recipe                    | Title, category, image, instructions, and ingredients using formsets        |
| Ingredient Search             | AJAX-powered with Select2, results dynamically returned                     |
| Save Favorite                 | One-click save/unsave to personal list                                      |
| Dark Mode Toggle              | Retains preference via `localStorage`                                       |
| Profile Page                  | User recipes, avatar, bio                                                   |
| Admin Dashboard               | Available to superusers for moderation                                      |

---

## ✅ Manual Testing Table

| Feature                       | Test Description                            | Expected Outcome          | Status     |
|-------------------------------|---------------------------------------------|---------------------------|------------|
| Register User                 | Fill and submit form                        | New user created          | Pass       |
| Add Recipe                    | Submit form with ingredients                | Recipe saved              | Pass       |
| Favorite Toggle               | Click heart icon                            | Recipe added/removed      | Pass       |
| Ingredient Search             | Type “sugar” in ingredient field            | Relevant results appear   | Pass       |
| Dark Mode                     | Toggle switch                               | Colors inverted           | Pass       |
| Admin Login                   | Login as superuser                          | Dashboard access          | Pass       |
| Update Profile                | Change avatar and bio                       | Profile updated           | Pass       |
| Mobile Layout                 | Open site on phone                          | Layout responsive         | Pass       |

---

## 🎯 First-Time Visitor Goals

- Understand what the platform does upon landing.
- Explore recent and popular recipes.
- View single recipe details without account.
- Use search to quickly find relevant dishes.
- Easily register an account to contribute recipes.

---

## Returning Visitor Goals

- Log in and access saved (favorite) recipes.
- Add or manage personal recipes.
- Update profile with avatar and bio.
- Search by ingredients and categories.

---

## Design

- **Font**: 'Quicksand' via Google Fonts.
- **Color Theme**: Earthy tones with Bootstrap support.
- **Dark Mode**: Uses `body.dark-mode` class to switch palette.
- **Buttons & Cards**: Styled with consistent Bootstrap 5 and custom shadows.
- **CSS**: Clean, commented, organized by sections (base, dark mode, recipe cards, forms).

---

## 🧪 Validator Testing

### ✅ HTML Validation
Validated via W3C Validator

- ![Index HTML](README_IMAGES/indextest.png)
- ![Profile HTML](README_IMAGES/profiletest.png)
- ![My Recipes HTML](README_IMAGES/myrecipetest.png)
- ![My Favorites HTML](README_IMAGES/myfavoritetest.png)
- ![Add Recipe HTML](README_IMAGES/addrecipetest.png)
- ![Admin Page HTML](README_IMAGES/adminpagetest.png)

### ✅ CSS Validation  
- ![CSS Validator](README_IMAGES/csstest.png)

### ✅ JavaScript Validation (JSHint)
- ![JS DOM Test](README_IMAGES/jsdmtest.png)
- ![Add Recipe JS Test](README_IMAGES/addrecipejstest.png)
- ![Edit Recipe JS Test](README_IMAGES/editrecipejstest.png)
- ![Recipes JS Test](README_IMAGES/recipesjstest.png)
- ![Recipe Detail JS Test](README_IMAGES/recipedetailjstest.png)

### ✅ Python Validation (Code Institute Linter)
- ![Forms.py](README_IMAGES/formspytest.png)
- ![Models.py](README_IMAGES/modelspytest.png)
- ![Views.py](README_IMAGES/viewstest.png)
- ![Urls.py](README_IMAGES/urlstest.png)

---

## 🚀 Performance

Tested via Google Lighthouse  
![Performance](README_IMAGES/perfomancetest.png)

- **Performance**: 96%
- **Accessibility**: 88%
- **Best Practices**: 93%
- **SEO**: 91%

---

## 📱 Devices Tested

The following devices were used to test responsiveness:

- **Mobile**: iPhone 16, iPhone 15, Samsung Galaxy S23 Ultra  
- **Tablet**: iPad Air, Xiaomi Redmi Tab Pro  
- **Desktop**: MacBook Pro, Windows PC (1920x1080 resolution)

### Results

- **Mobile**: All elements were displayed correctly, and the layout was adjusted to fit the smaller screen. Navigation, buttons, and functionality were fully operational. **Works as expected.**
- **Tablet**: The site scaled perfectly for medium-sized screens, maintaining visual hierarchy and ease of navigation. **Works as expected.**
- **Desktop**: The full layout was displayed as intended, with no visual or functional issues. **Works as expected.**

---

## 💡 Future Features

- Recipe commenting and discussions
- User-to-user following system
- Dietary filters (vegan, gluten-free)
- Shareable recipe links with previews

---

## 🛠️ Deployment

Hosted on **Heroku**: [Live Site](https://shared-spoon-f2d629a69afc.herokuapp.com)  
Code: [GitHub Repository](https://github.com/martiiann/shared-spoon)

---

## 🐞 Debugging & Problem Solving

During development, I encountered and resolved several issues using Chrome DevTools, Django logs, and Heroku CLI. Key fixes included:

- **AJAX Ingredient Search**: Corrected a CSRF token issue and adjusted `data-url` in the dynamic form.
- **Static Files on Heroku**: Solved by setting up Whitenoise, ensuring `collectstatic` ran, and configuring `STATIC_ROOT`.
- **Formset Save Errors**: Fixed by using `commit=False` and linking child form data to the parent `Recipe` object.
- **404 on Recipe Detail**: Traced to a missing `pk` in the URL — resolved with the correct pattern and view query.

Tools used included `console.log()`, Django’s debug messages, and `heroku logs --tail`.

---

## 🧠 Lessons Learned

This project deepened my understanding of Django and full-stack development. I learned how to:

- Build dynamic, user-friendly forms with formsets and Select2
- Use AJAX to enhance user experience in real-time without page reloads
- Implement responsive layouts using Bootstrap and dark mode customization
- Store media and sensitive data securely in production using environment variables
- Test, validate, and deploy a fully functional site on Heroku

If given more time, I would further expand features such as recipe commenting and a user-following system. This project helped me build confidence in deploying secure, scalable, and user-centered web applications.

---

## Acknowledgments
- Special thanks to my mentors **Marko** and **Moritz** for their invaluable guidance throughout my project.
- I would like to thank the tutor support team at **Code Institute** for their assistance.
- A big thank you to the entire **Code Institute** for providing me with the opportunity to attend this course and work on this project.