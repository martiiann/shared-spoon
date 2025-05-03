from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .models import Recipe, Rating, Profile, Ingredient, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientFormSet, ProfileForm
from accounts.decorators import admin_required


User = get_user_model()


@login_required
@admin_required
def admin_dashboard(request):
    context = {
        'user_count': User.objects.count(),
        'recipe_count': Recipe.objects.count(),
        'ingredient_count': Ingredient.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)


@method_decorator([login_required, admin_required], name='dispatch')
class RecipeListView(ListView):
    model = Recipe
    template_name = 'admin/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 20


@method_decorator([login_required, admin_required], name='dispatch')
class RecipeCreateView(CreateView):
    model = Recipe
    fields = [
        'user', 'title', 'description',
        'instructions', 'category', 'image'
    ]
    template_name = 'admin/recipe_form.html'
    success_url = reverse_lazy('recipes:admin_recipe_list')


@method_decorator([login_required, admin_required], name='dispatch')
class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = [
        'user', 'title', 'description',
        'instructions', 'category', 'image'
    ]
    template_name = 'admin/recipe_form.html'
    success_url = reverse_lazy('recipes:admin_recipe_list')


@method_decorator([login_required, admin_required], name='dispatch')
class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'admin/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipes:admin_recipe_list')


@method_decorator([login_required, admin_required], name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 20


@method_decorator([login_required, admin_required], name='dispatch')
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'admin/ingredient_list.html'
    context_object_name = 'ingredients'
    paginate_by = 20


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

    user_recipes_count = 0
    if request.user.is_authenticated:
        user_recipes_count = Recipe.objects.filter(user=request.user).count()

        user_ratings = Rating.objects.filter(
            user=request.user,
            recipe__in=page_obj
        ).select_related('recipe')
        rating_dict = {r.recipe.id: r for r in user_ratings}
        for recipe in page_obj:
            recipe.user_rating = rating_dict.get(recipe.id)

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


def register(request):
    if request.user.is_authenticated:
        return redirect('recipes:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            msg = 'Welcome! Your account has been created.'
            messages.success(request, msg)
            return redirect('recipes:index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            formset.instance = recipe
            formset.save()

            messages.success(request, 'Recipe added successfully!')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'formset': formset,
    })


def manage_ingredients(request):
    q = request.GET.get('q', '')
    ingredients = Ingredient.objects.filter(name__icontains=q).order_by('name')
    results = [{'id': ing.id, 'text': ing.name} for ing in ingredients]
    return JsonResponse({'results': results})



@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = RecipeIngredientFormSet(
            request.POST, request.FILES, instance=recipe
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {
        'form': form,
        'formset': formset,
    })


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully.')
        return redirect('recipes:my')
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})


def recipe_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'all')

    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(title__icontains=query)

    if category != 'all':
        recipes = recipes.filter(category=category)

    if request.user.is_authenticated:
        user_ratings = Rating.objects.filter(
            user=request.user,
            recipe__in=recipes
        ).select_related('recipe')

        rating_dict = {rating.recipe_id: rating for rating in user_ratings}

        for recipe in recipes:
            recipe.user_rating = rating_dict.get(recipe.id)

    user_recipes_count = 0
    if request.user.is_authenticated:
        user_recipes_count = Recipe.objects.filter(user=request.user).count()

    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
        'user_recipes_count': user_recipes_count,
    }
    return render(request, 'recipes/index.html', context)


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/my_recipes.html', {'page_obj': page_obj})


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


@login_required
def my_favorites(request):
    recipes = Recipe.objects.filter(liked_by=request.user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/my_favorites.html', {'page_obj': page_obj})


def recipe_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related('recipe_ingredients__ingredient'),
        pk=pk
    )

    ingredients = recipe.recipe_ingredients.select_related('ingredient').all()

    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            user=request.user,
            recipe=recipe
        ).first()

    is_favorite = (
        request.user.is_authenticated and
        recipe.liked_by.filter(id=request.user.id).exists()
    )

    avg_rating = recipe.ratings.aggregate(avg=Avg('value'))['avg'] or 0
    rating_count = recipe.ratings.count()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
        'avg_rating': round(avg_rating, 1),
        'rating_count': rating_count,
    })


@login_required
def rate_recipe(request, recipe_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        value = int(request.POST.get('rating', 0))
        Rating.objects.update_or_create(
            user=request.user,
            recipe=recipe,
            defaults={'value': value}
        )
        avg_rating = Rating.objects.filter(
            recipe=recipe
        ).aggregate(avg=Avg('value'))['avg']
        rating_count = Rating.objects.filter(recipe=recipe).count()
        return JsonResponse({
            'success': True,
            'avg_rating': round(avg_rating, 1),
            'rating_count': rating_count
        })
    return JsonResponse({'success': False})


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('recipes:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'recipes/profile.html', {
        'profile': profile,
        'form': form,
    })


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    recipes = Recipe.objects.filter(user=user)
    return render(request, 'recipes/public_profile.html', {
        'user_profile': user,
        'profile': profile,
        'recipes': recipes
    })
