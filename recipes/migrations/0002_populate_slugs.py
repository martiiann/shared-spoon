from django.db import migrations
from django.utils.text import slugify
import itertools

def generate_unique_slug(Model, title, current_pk=None):
    """Generate a unique slug for recipes"""
    base_slug = slugify(title)[:200]
    unique_slug = base_slug
    for i in itertools.count(1):
        if not Model.objects.filter(slug=unique_slug).exclude(pk=current_pk).exists():
            break
        unique_slug = f"{base_slug}-{i}"[:200]
    return unique_slug

def populate_slugs(apps, schema_editor):
    """Populate slug field for existing recipes"""
    Recipe = apps.get_model('recipes', 'Recipe')
    for recipe in Recipe.objects.filter(slug__isnull=True):
        recipe.slug = generate_unique_slug(Recipe, recipe.title, recipe.pk)
        recipe.save(update_fields=['slug'])

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]