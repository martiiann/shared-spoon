from django.urls import path
from . import views
from .views import admin_dashboard

app_name = 'recipes'  

urlpatterns = [
    # Public routes
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    
    # Recipe CRUD
    path('recipes/add/', views.add_recipe, name='add'),
    path('recipes/my/', views.my_recipes, name='my'),
    path('recipes/edit/<int:pk>/', views.edit_recipe, name='edit_recipe'),
    path('recipes/delete/<int:pk>/', views.delete_recipe, name='delete_recipe'),
    
    # Favorites system
    path('recipes/favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('recipes/favorites/', views.my_favorites, name='favorites'),

    # Ratings
    path('rate-recipe/<int:recipe_id>/', views.rate_recipe, name='rate_recipe'),

    # Profile
    path('account/profile/', views.profile_view, name='profile'),
    path('user/<str:username>/', views.public_profile, name='public_profile'),
    
    # AJAX endpoints
    path('api/ingredients/', views.manage_ingredients, name='ingredient_search'), 

    #Admin
    path('app-admin/', admin_dashboard, name='app_admin_dashboard'),
    path('app-admin/recipes/',        views.RecipeListView.as_view(),    name='admin_recipe_list'),
    path('app-admin/recipes/create/', views.RecipeCreateView.as_view(),  name='admin_recipe_create'),
    path('app-admin/recipes/<int:pk>/edit/',   views.RecipeUpdateView.as_view(), name='admin_recipe_edit'),
    path('app-admin/recipes/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='admin_recipe_delete'),
    path('app-admin/users/', views.UserListView.as_view(), name='admin_user_list'),
    path('app-admin/ingredients/', views.IngredientListView.as_view(), name='admin_ingredient_list'),
]
