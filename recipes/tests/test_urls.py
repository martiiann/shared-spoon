from django.test import SimpleTestCase
from django.urls import reverse

class TestURLRoutes(SimpleTestCase):
    def test_named_routes_reverse_and_resolve(self):
        url_map = {
            'recipes:index': '/',
            'recipes:register': '/register/',
            'recipes:add': '/recipes/add/',
            'recipes:my': '/recipes/my/',
            'recipes:favorites': '/recipes/favorites/',
            'recipes:profile': '/account/profile/',
            'recipes:ingredient_search': '/api/ingredients/',
            'recipes:app_admin_dashboard': '/app-admin/',
            'recipes:admin_recipe_list': '/app-admin/recipes/',
            'recipes:admin_recipe_create': '/app-admin/recipes/create/',
            'recipes:admin_user_list': '/app-admin/users/',
            'recipes:admin_ingredient_list': '/app-admin/ingredients/',
        }

        for name, path in url_map.items():
            with self.subTest(name=name):
                self.assertEqual(reverse(name), path)

    def test_dynamic_routes_reverse(self):
        self.assertEqual(reverse('recipes:recipe_detail', args=[5]), '/recipe/5/')
        self.assertEqual(reverse('recipes:edit_recipe', args=[10]), '/recipes/edit/10/')
        self.assertEqual(reverse('recipes:delete_recipe', args=[15]), '/recipes/delete/15/')
        self.assertEqual(reverse('recipes:toggle_favorite', args=[20]), '/recipes/favorite/20/')
        self.assertEqual(reverse('recipes:rate_recipe', args=[25]), '/rate-recipe/25/')
        self.assertEqual(reverse('recipes:admin_recipe_edit', args=[30]), '/app-admin/recipes/30/edit/')
        self.assertEqual(reverse('recipes:admin_recipe_delete', args=[35]), '/app-admin/recipes/35/delete/')
        self.assertEqual(reverse('recipes:public_profile', args=['jane']), '/user/jane/')
