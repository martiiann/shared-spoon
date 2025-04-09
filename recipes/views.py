from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm

def index(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/index.html', {'recipes': recipes})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login after registering
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
