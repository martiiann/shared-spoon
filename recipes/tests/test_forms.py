from django.test import TestCase
from recipes.forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet, ProfileForm
from recipes.models import Ingredient, Recipe, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeFormTest(TestCase):
    def test_valid_data(self):
        form = RecipeForm(data={
            'title': 'Pizza',
            'description': 'Delicious pizza',
            'instructions': 'Bake at 200C',
            'category': 'lunch',
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form = RecipeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

class RecipeIngredientFormTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Cheese')

    def test_valid_ingredient_form(self):
        form = RecipeIngredientForm(data={
            'ingredient': self.ingredient.id,
            'quantity': '200g',
            'notes': 'grated',
        })
        self.assertTrue(form.is_valid())

    def test_missing_ingredient(self):
        form = RecipeIngredientForm(data={'quantity': '1 cup'})
        self.assertFalse(form.is_valid())
        self.assertIn('ingredient', form.errors)

class RecipeIngredientFormSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Soup',
            description='Hot soup',
            instructions='Boil water',
            category='dinner'
        )
        self.ingredient = Ingredient.objects.create(name='Water')

    def test_formset_with_valid_data(self):
        formset_data = {
            'recipe_ingredients-TOTAL_FORMS': '1',
            'recipe_ingredients-INITIAL_FORMS': '0',
            'recipe_ingredients-MIN_NUM_FORMS': '1',
            'recipe_ingredients-MAX_NUM_FORMS': '1000',
            'recipe_ingredients-0-ingredient': self.ingredient.id,
            'recipe_ingredients-0-quantity': '2 cups',
            'recipe_ingredients-0-notes': '',
        }
        formset = RecipeIngredientFormSet(data=formset_data, instance=self.recipe, prefix='recipe_ingredients')
        self.assertTrue(formset.is_valid())

class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jane', password='pass')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_form_valid(self):
        form = ProfileForm(data={
            'bio': 'Loves cooking',
            'website': 'https://example.com',
            'location': 'Paris'
        }, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_empty_profile_form_still_valid(self):
        form = ProfileForm(data={}, instance=self.profile)
        self.assertTrue(form.is_valid())
