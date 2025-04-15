from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the ingredient (e.g. 'Flour', 'Sugar')"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description or notes about the ingredient"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ingredient_detail', kwargs={'pk': self.pk})


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast 🥞'),
        ('lunch', 'Lunch 🥪'),
        ('dinner', 'Dinner 🍝'),
        ('dessert', 'Dessert 🍰'),
        ('vegan', 'Vegan 🥗'),
        ('snack', 'Snack 🍪'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(
        max_length=200,
        help_text="Title of your recipe"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Automatically generated URL-friendly version of the title"
    )
    description = models.TextField(
        help_text="Brief description of the recipe"
    )
    instructions = models.TextField(
        help_text="Step-by-step cooking instructions"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        help_text="Category of the recipe"
    )
    image = models.ImageField(
        upload_to='recipe_images/',
        blank=True,
        null=True,
        help_text='Upload a high-quality image of your recipe'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(
        User,
        related_name='favorite_recipes',
        blank=True,
        verbose_name='Users who liked this recipe'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
        ]
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200]
            self.slug = base_slug
            counter = 1
            while Recipe.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    @property
    def avg_rating(self):
        """Calculate average rating with caching"""
        if not hasattr(self, '_avg_rating'):
            self._avg_rating = self.ratings.aggregate(Avg('value'))['value__avg'] or 0
        return self._avg_rating

    @property
    def rating_count(self):
        """Count of all ratings with caching"""
        if not hasattr(self, '_rating_count'):
            self._rating_count = self.ratings.count()
        return self._rating_count

    def user_rating(self, user):
        """Get a user's rating for this recipe"""
        try:
            return self.ratings.get(user=user).value
        except Rating.DoesNotExist:
            return None


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='used_in_recipes'
    )
    quantity = models.CharField(
        max_length=50,
        blank=True,
        help_text="Amount needed (e.g. '1 cup', '2 tablespoons')"
    )
    notes = models.CharField(
        max_length=100,
        blank=True,
        help_text="Special preparation notes (e.g. 'chopped', 'at room temperature')"
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Position in ingredient list"
    )

    class Meta:
        ordering = ['order']
        unique_together = ('recipe', 'ingredient')
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'

    def __str__(self):
        parts = []
        if self.quantity:
            parts.append(self.quantity)
        parts.append(self.ingredient.name)
        if self.notes:
            parts.append(f"({self.notes})")
        return ' '.join(parts)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default-avatar.png'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        default=''
    )
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    def get_absolute_url(self):
        return reverse('profile')


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings_given'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    value = models.PositiveSmallIntegerField(
        choices=[(i, f'{i} star{"s" if i > 1 else ""}') for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'recipe')
        ordering = ['-created_at']
        verbose_name = 'Recipe Rating'
        verbose_name_plural = 'Recipe Ratings'

    def __str__(self):
        return f'{self.user.username} rated {self.recipe.title} {self.value} stars'