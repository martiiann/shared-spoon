from django.shortcuts import render
from .models import Recipe

def index(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/index.html', {'recipes': recipes})
