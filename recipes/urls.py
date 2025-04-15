from django.urls import path
from . import views

app_name = 'recipes'  

urlpatterns = [
    # Public routes
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('recipe/<int:pk>/', views.recipe_detail, name='detail'),  
    
    # Recipe CRUD
    path('recipes/add/', views.add_recipe, name='add'),
    path('recipes/my/', views.my_recipes, name='my'),
    path('recipes/edit/<int:pk>/', views.edit_recipe, name='edit'),
    path('recipes/delete/<int:pk>/', views.delete_recipe, name='delete'),
    
    # Favorites system
    path('recipes/favorite/<int:pk>/', views.toggle_favorite, name='favorite'),
    path('recipes/favorites/', views.my_favorites, name='favorites'),
    
    # Ratings
    path('recipes/rate/<int:pk>/', views.rate_recipe, name='rate'),
    
    # Profile
    path('account/profile/', views.profile_view, name='profile'),
    
    # AJAX endpoints
    path('api/ingredients/', views.manage_ingredients, name='ingredient_search'),  
]