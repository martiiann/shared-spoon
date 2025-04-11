from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import RecipeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

# View for the home page
def index(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        recipes = recipes.filter(title__icontains=query)
    if category and category != 'all':
        recipes = recipes.filter(category=category)

    paginator = Paginator(recipes, 6)  # Show 6 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_recipes_count = 0
    if request.user.is_authenticated:
        user_recipes_count = Recipe.objects.filter(user=request.user).count()

    return render(request, 'recipes/index.html', {
        'recipes': page_obj.object_list,
        'page_obj': page_obj,
        'selected_category': category,
        'query': query,
        'user_recipes_count': user_recipes_count,
    })

# Register view for creating a new account
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# View to add a recipe (logged-in users only)
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Ensure the logged-in user is associated with the recipe
            recipe.save()
            messages.success(request, "Recipe added successfully!")
            return redirect('my_recipes')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

# View to display the user's recipes
@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})

# View to toggle a recipe as favorite
@login_required
def toggle_favorite(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.liked_by.filter(id=request.user.id).exists():
        recipe.liked_by.remove(request.user)
    else:
        recipe.liked_by.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))

# View to display the user's favorite recipes
@login_required
def my_favorites(request):
    recipes = request.user.favorite_recipes.all().order_by('-created_at')
    return render(request, 'recipes/my_favorites.html', {'recipes': recipes})

# View to edit a recipe (logged-in users only)
@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.user != request.user:
        messages.error(request, "You can only edit your own recipes.")
        return redirect('my_recipes')

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated!")
            return redirect('my_recipes')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form})

# View to delete a recipe (logged-in users only)
@login_required
def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.user == request.user:
        recipe.delete()
        messages.success(request, "Recipe deleted!")
    else:
        messages.error(request, "You can only delete your own recipes.")
    return redirect('my_recipes')

# View to display the details of a recipe
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
