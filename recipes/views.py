from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.views.decorators.http import require_POST
from .models import Recipe, Rating, Profile, RecipeIngredient, Ingredient
from .forms import RecipeForm, ProfileForm, RecipeIngredientFormSet

def index(request):
    """
    Homepage view showing all recipes with filtering and pagination
    """
    recipes = Recipe.objects.annotate(
        avg_rating=Avg('ratings__value')
    ).prefetch_related(
        'recipe_ingredients__ingredient',
        'ratings'
    ).order_by('-created_at')

    # Filtering
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(recipe_ingredients__ingredient__name__icontains=query)
        ).distinct()
        
    if category and category != 'all':
        recipes = recipes.filter(category=category)

    # Pagination
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/index.html', {
        'page_obj': page_obj,
        'selected_category': category,
        'query': query,
        'user_recipes_count': request.user.recipes.count() if request.user.is_authenticated else 0,
    })

def register(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Auto-create profile
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_recipe(request):
    """
    View for adding new recipes with ingredients formset
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredients')
        
        if form.is_valid() and formset.is_valid():
            try:
                recipe = form.save(commit=False)
                recipe.user = request.user
                recipe.save()
                
                # Save ingredients with order
                instances = formset.save(commit=False)
                for idx, instance in enumerate(instances):
                    instance.recipe = recipe
                    instance.order = idx
                    instance.save()
                
                messages.success(request, "Recipe added successfully!")
                return redirect('my_recipes')
                
            except Exception as e:
                messages.error(request, f"Error saving recipe: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            for form in formset.forms:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Ingredient {field}: {error}")
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet(prefix='ingredients', queryset=RecipeIngredient.objects.none())
    
    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'ingredient_formset': formset
    })

@login_required
def edit_recipe(request, recipe_id):
    """
    View for editing existing recipes with ingredients formset
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = RecipeIngredientFormSet(
            request.POST, 
            prefix='ingredients',
            instance=recipe
        )
        
        if form.is_valid() and formset.is_valid():
            form.save()
            
            # Update ingredients with order
            instances = formset.save(commit=False)
            for idx, instance in enumerate(instances):
                instance.order = idx
                instance.save()
            formset.save_m2m()
            
            # Delete marked ingredients
            for obj in formset.deleted_objects:
                obj.delete()
                
            messages.success(request, "Recipe updated!")
            return redirect('my_recipes')
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(
            prefix='ingredients',
            instance=recipe
        )
    
    return render(request, 'recipes/edit_recipe.html', {
        'form': form,
        'ingredient_formset': formset,
        'recipe': recipe
    })

@login_required
def my_recipes(request):
    """
    View showing all recipes by the current user
    """
    recipes = Recipe.objects.filter(user=request.user).prefetch_related(
        'recipe_ingredients__ingredient'
    ).order_by('-created_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})

@login_required
def toggle_favorite(request, recipe_id):
    """
    View to add/remove recipe from favorites
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.liked_by.filter(id=request.user.id).exists():
        recipe.liked_by.remove(request.user)
        messages.success(request, "Removed from favorites!")
    else:
        recipe.liked_by.add(request.user)
        messages.success(request, "Added to favorites!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))

@login_required
def my_favorites(request):
    """
    View showing all favorited recipes
    """
    recipes = request.user.favorite_recipes.prefetch_related(
        'recipe_ingredients__ingredient'
    ).order_by('-created_at')
    return render(request, 'recipes/my_favorites.html', {'recipes': recipes})

@login_required
def delete_recipe(request, recipe_id):
    """
    View to delete a recipe
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.delete()
    messages.success(request, "Recipe deleted!")
    return redirect('my_recipes')

def recipe_detail(request, pk):
    """
    Detailed view for a single recipe
    """
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related(
            'recipe_ingredients__ingredient',
            'ratings'
        ),
        pk=pk
    )
    
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            user=request.user,
            recipe=recipe
        ).first()

    context = {
        'recipe': recipe,
        'user_rating': user_rating,
        'avg_rating': recipe.ratings.aggregate(Avg('value'))['value__avg'] or 0,
    }
    return render(request, 'recipes/recipe_detail.html', context)

@require_POST
def rate_recipe(request, recipe_id):
    """
    AJAX view for rating recipes
    """
    if request.user.is_authenticated and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            rating_value = int(request.POST.get('rating'))
            
            if not 1 <= rating_value <= 5:
                return JsonResponse({'error': 'Rating must be 1-5'}, status=400)
            
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                recipe=recipe,
                defaults={'value': rating_value}
            )
            
            return JsonResponse({
                'success': True,
                'avg_rating': recipe.avg_rating,
                'rating_count': recipe.ratings.count(),
                'user_rating': rating_value
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def profile_view(request):
    """
    View for user profile management
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'recipes/profile.html', {'form': form})

@login_required
def manage_ingredients(request):
    """
    AJAX endpoint for ingredient search (used by Select2)
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.POST.get('q', '')
        ingredients = Ingredient.objects.filter(
            name__icontains=query
        ).values('id', 'name')[:10]
        return JsonResponse(list(ingredients), safe=False)
    return JsonResponse([], safe=False)