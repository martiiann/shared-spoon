from django.db import migrations, models

def verify_no_nulls(apps, schema_editor):
    Recipe = apps.get_model('recipes', 'Recipe')
    if Recipe.objects.filter(slug__isnull=True).exists():
        raise ValueError("Null slugs found! Run 0002_populate_slugs first.")

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0002_populate_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, blank=True),
        ),
        migrations.RunPython(verify_no_nulls),
    ]