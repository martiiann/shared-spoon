from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Recipe, Rating, Profile, Ingredient
from .forms import RecipeForm, RecipeIngredientFormSet, ProfileForm
from django.db.models import Avg


# Homepage (Index)
def index(request):
    query = request.GET.get('q')
    selected_category = request.GET.get('category', 'all')

    recipes = Recipe.objects.all()
    if query:
        recipes = recipes.filter(title__icontains=query)
    if selected_category != 'all':
        recipes = recipes.filter(category=selected_category)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Count of recipes the user created
    user_recipes_count = 0
    if request.user.is_authenticated:
        user_recipes_count = Recipe.objects.filter(user=request.user).count()

        # Attach user_ratings
        user_ratings = Rating.objects.filter(
            user=request.user,
            recipe__in=page_obj
        ).select_related('recipe')
        rating_dict = {r.recipe.id: r for r in user_ratings}
        for recipe in page_obj:
            recipe.user_rating = rating_dict.get(recipe.id)

        # **NEW**: Attach is_favorite flag
        fav_ids = set(
            Recipe.objects
                  .filter(liked_by=request.user)
                  .values_list('id', flat=True)
        )
        for recipe in page_obj:
            recipe.is_favorite = (recipe.id in fav_ids)

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': selected_category,
        'user_recipes_count': user_recipes_count,
    }
    return render(request, 'recipes/index.html', context)

# Register User
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Add Recipe
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # 1️⃣ Save the recipe so we have a PK to attach ingredients to
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            # 2️⃣ Now bind the POST data to a formset *on* that recipe
            formset = RecipeIngredientFormSet(request.POST, request.FILES, instance=recipe)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Recipe added successfully!')
                return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            # If the main form is invalid, still bind the formset so its errors show
            formset = RecipeIngredientFormSet(request.POST, request.FILES)
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()  # unbound on GET

    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'formset': formset,
    })
# Ingredient Search (AJAX API) — THIS IS CORRECT NOW
def manage_ingredients(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        q = request.GET.get('q', '')
        ingredients = Ingredient.objects.filter(name__icontains=q).order_by('name')
        results = [{'id': ing.id, 'text': ing.name} for ing in ingredients]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

# Edit Recipe
@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipes:my')
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {
        'form': form,
        'formset': formset,
    })

# Delete Recipe
@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully.')
        return redirect('recipes:my')
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})

def recipe_list(request):
    # Get search query and category filter
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'all')
    
    # Start with all recipes
    recipes = Recipe.objects.all()
    
    # Apply filters
    if query:
        recipes = recipes.filter(title__icontains=query)
    
    if category != 'all':
        recipes = recipes.filter(category=category)
    
    # Add user rating information if authenticated
    if request.user.is_authenticated:
        # Prefetch ratings for efficiency
        user_ratings = Rating.objects.filter(
            user=request.user,
            recipe__in=recipes
        ).select_related('recipe')
        
        # Create a dictionary for quick lookup
        rating_dict = {rating.recipe_id: rating for rating in user_ratings}
        
        # Add user_rating to each recipe
        for recipe in recipes:
            recipe.user_rating = rating_dict.get(recipe.id)
    
    # Count user's recipes (for the "Add Your First Recipe" button)
    user_recipes_count = 0
    if request.user.is_authenticated:
        user_recipes_count = Recipe.objects.filter(user=request.user).count()
    
    # Pagination
    paginator = Paginator(recipes, 12)  # Show 12 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'user_recipes_count': user_recipes_count,
    }
    return render(request, 'recipes/index.html', context)

# My Recipes (List only user's own recipes)
@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/my_recipes.html', {'page_obj': page_obj})

# Toggle Favorite
@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.liked_by.filter(id=request.user.id).exists():
        recipe.liked_by.remove(request.user)
        favorited = False
        msg = 'Removed from favorites.'
    else:
        recipe.liked_by.add(request.user)
        favorited = True
        msg = 'Recipe saved to favorites!'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'favorited': favorited,
            'liked_by_count': recipe.liked_by.count(),
            'message': msg
        })

    return redirect(request.META.get('HTTP_REFERER', 'recipes:index'))

# My Favorites
@login_required
def my_favorites(request):
    recipes = Recipe.objects.filter(liked_by=request.user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/my_favorites.html', {'page_obj': page_obj})

# Recipe Detail Page
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, recipe=recipe).first()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = recipe.liked_by.filter(id=request.user.id).exists()

    avg_rating = recipe.ratings.aggregate(avg=Avg('value'))['avg'] or 0
    rating_count = recipe.ratings.count()

    context = {
        'recipe': recipe,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
        'avg_rating': round(avg_rating, 1),
        'rating_count': rating_count,
    }
    return render(request, 'recipes/recipe_detail.html', context)

# Rate Recipe
@login_required
def rate_recipe(request, recipe_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        value = int(request.POST.get('rating', 0))
        rating, created = Rating.objects.update_or_create(
            user=request.user, recipe=recipe,
            defaults={'value': value}
        )
        avg_rating = Rating.objects.filter(recipe=recipe).aggregate(avg=Avg('value'))['avg']
        rating_count = Rating.objects.filter(recipe=recipe).count()
        return JsonResponse({'success': True, 'avg_rating': round(avg_rating, 1), 'rating_count': rating_count})
    return JsonResponse({'success': False})

# Profile View
@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('recipes:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'recipes/profile.html', {'profile': profile, 'form': form})

def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    recipes = Recipe.objects.filter(user=user)
    return render(request, 'recipes/public_profile.html', {
        'user_profile': user,
        'profile': profile,
        'recipes': recipes
    })