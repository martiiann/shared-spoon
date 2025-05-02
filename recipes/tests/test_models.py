from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from recipes.models import Ingredient, Recipe, RecipeIngredient, Profile, Rating

User = get_user_model()

class IngredientModelTest(TestCase):
    def test_string_representation(self):
        ingredient = Ingredient.objects.create(name="Sugar")
        self.assertEqual(str(ingredient), "Sugar")

    @patch('recipes.models.reverse', return_value='/ingredient/123/')
    def test_get_absolute_url(self, mock_reverse):
        ingredient = Ingredient.objects.create(name="Flour")
        self.assertEqual(ingredient.get_absolute_url(), '/ingredient/123/')

class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_string_representation(self):
        recipe = Recipe.objects.create(user=self.user, title="Pasta", description="desc", instructions="instr", category="dinner")
        self.assertEqual(str(recipe), "Pasta")

    def test_slug_auto_generation(self):
        recipe = Recipe.objects.create(user=self.user, title="Test Slug", description="desc", instructions="instr", category="lunch")
        self.assertTrue(recipe.slug.startswith("test-slug"))

    @patch('recipes.models.reverse', return_value='/recipe/123/test-slug/')
    def test_get_absolute_url(self, mock_reverse):
        recipe = Recipe.objects.create(user=self.user, title="Soup", description="desc", instructions="instr", category="dinner")
        self.assertEqual(recipe.get_absolute_url(), '/recipe/123/test-slug/')

class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='pass')
        self.recipe = Recipe.objects.create(user=self.user, title="Cake", description="desc", instructions="instr", category="dessert")
        self.ingredient = Ingredient.objects.create(name="Flour")

    def test_string_representation(self):
        ri = RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient, quantity="2 cups", notes="sifted")
        self.assertIn("2 cups", str(ri))
        self.assertIn("Flour", str(ri))
        self.assertIn("(sifted)", str(ri))

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='pass')

    def test_string_representation(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), "profileuser's Profile")

    @patch('recipes.models.reverse', return_value='/profile/')
    def test_get_absolute_url(self, mock_reverse):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.get_absolute_url(), '/profile/')

class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rateuser', password='pass')
        self.recipe = Recipe.objects.create(user=self.user, title="Pizza", description="desc", instructions="instr", category="lunch")

    def test_string_representation(self):
        rating = Rating.objects.create(user=self.user, recipe=self.recipe, value=4)
        self.assertIn("4 stars", str(rating))
