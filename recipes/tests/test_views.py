from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from recipes.models import Recipe, Ingredient, RecipeIngredient, Profile, Rating

User = get_user_model()

class ViewTestBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.admin = User.objects.create_user(
            username='admin', password='adminpass',
            email='admin@example.com', is_staff=True, is_superuser=True
        )
        Profile.objects.create(user=self.user)
        Profile.objects.create(user=self.admin)
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Test Recipe',
            description='Test Description',
            instructions='Step 1: do something',
            category='lunch'
        )
        self.ingredient = Ingredient.objects.create(name='Salt')
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity='1 tsp'
        )

class EditRecipeViewTest(ViewTestBase):
    def test_get_edit_page_as_owner(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('recipes:edit_recipe', args=[self.recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/edit_recipe.html')

    def test_post_valid_edit(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('recipes:edit_recipe', args=[self.recipe.id])
        data = {
            'title': 'Updated Recipe',
            'description': 'Updated description',
            'instructions': 'Updated instructions',
            'category': 'dinner',
            'recipe_ingredients-TOTAL_FORMS': '1',
            'recipe_ingredients-INITIAL_FORMS': '1',
            'recipe_ingredients-MIN_NUM_FORMS': '0',
            'recipe_ingredients-MAX_NUM_FORMS': '1000',
            'recipe_ingredients-0-id': str(self.recipe_ingredient.id),
            'recipe_ingredients-0-ingredient': str(self.ingredient.id),
            'recipe_ingredients-0-quantity': '2 tsp',
            'recipe_ingredients-0-notes': '',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Updated Recipe')

class DeleteRecipeViewTest(ViewTestBase):
    def test_delete_recipe(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('recipes:delete_recipe', args=[self.recipe.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('recipes:my'))
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())

class RateRecipeAjaxTest(ViewTestBase):
    def test_rate_recipe_ajax_post(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('recipes:rate_recipe', args=[self.recipe.id])
        response = self.client.post(url, {'rating': '4'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Rating.objects.filter(user=self.user, recipe=self.recipe).exists())

class ToggleFavoriteTest(ViewTestBase):
    def test_toggle_favorite_ajax(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('recipes:toggle_favorite', args=[self.recipe.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.recipe.liked_by.filter(id=self.user.id).exists())

class MyRecipesViewTest(ViewTestBase):
    def test_my_recipes_view(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('recipes:my'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/my_recipes.html')


class ProfileViewTest(ViewTestBase):
    def test_profile_view_get(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('recipes:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/profile.html')

    def test_profile_view_post(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('recipes:profile')
        data = {
            'bio': 'Updated bio',
            'location': 'Testville',
            'website': 'https://example.com',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')


class AdminRecipeViewsTest(ViewTestBase):
    def test_admin_recipe_list_view(self):
        self.client.login(username='admin', password='adminpass')
        try:
            url = reverse('recipes:admin_recipe_list')
        except NoReverseMatch:
            url = reverse('admin_recipe_list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 403])
