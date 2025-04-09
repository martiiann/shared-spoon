from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
]
