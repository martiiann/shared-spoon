from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
        ('vegan', 'Vegan'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    liked_by = models.ManyToManyField(User, related_name="favorite_recipes", blank=True)  

    def __str__(self):
        return self.title



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='default-avatar.png')  # Default image
    bio = models.TextField(max_length=500, blank=True, null=True)  # Optional bio field

    def __str__(self):
        return f'{self.user.username} Profile'

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')  # Prevent multiple ratings from the same user

    def __str__(self):
        return f'{self.recipe.title} - {self.value}⭐ by {self.user.username}'