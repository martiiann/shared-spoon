from django.urls import path
from . import views
from .views import profile_view

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
     path('profile/', profile_view, name='profile'),
]
