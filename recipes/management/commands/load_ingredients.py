from django.core.management.base import BaseCommand
from django.utils import timezone
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Loads a comprehensive list of common UK ingredients into the database'

    def handle(self, *args, **options):
        ingredients = [
            # Baking & Pantry
            ("Plain flour", "Common UK all-purpose flour for baking"),
            ("Self-raising flour", "Flour with added baking powder for cakes and sponges"),
            ("Caster sugar", "Fine white sugar used in baking"),
            ("Granulated sugar", "Standard white sugar"),
            ("Icing sugar", "Powdered sugar for dusting and icing"),
            ("Brown sugar", "Soft light brown sugar used in baking"),
            ("Bicarbonate of soda", "Baking soda for rising"),
            ("Baking powder", "Leavening agent"),
            ("Cornflour", "Cornstarch used for thickening sauces"),

            # Dairy & Eggs
            ("Butter", "Unsalted dairy butter"),
            ("Salted butter", "Salted variety of butter"),
            ("Milk", "Whole milk"),
            ("Semi-skimmed milk", "Reduced-fat milk"),
            ("Double cream", "Heavy cream"),
            ("Single cream", "Lighter cream for pouring"),
            ("Cheddar cheese", "Classic UK cheese"),
            ("Eggs", "Free range chicken eggs"),

            # Oils & Condiments
            ("Olive oil", "Extra virgin olive oil"),
            ("Vegetable oil", "Neutral cooking oil"),
            ("Sunflower oil", "Light oil for frying"),
            ("Vinegar", "Distilled white vinegar"),
            ("Balsamic vinegar", "Dark, sweet vinegar"),
            ("Soy sauce", "Used in Asian cuisine"),
            ("Tomato ketchup", "Classic tomato condiment"),
            ("Mayonnaise", "Egg-based dressing"),

            # Herbs & Spices
            ("Salt", "Table salt"),
            ("Sea salt", "Coarse salt crystals"),
            ("Black pepper", "Ground black pepper"),
            ("Chilli flakes", "Dried crushed chillies"),
            ("Paprika", "Mild red pepper powder"),
            ("Cumin", "Earthy spice used in curries"),
            ("Turmeric", "Golden yellow spice"),
            ("Coriander", "Ground coriander seeds"),
            ("Mixed herbs", "UK blend of dried herbs"),
            ("Basil", "Dried basil leaves"),
            ("Oregano", "Dried oregano leaves"),

            # Vegetables
            ("Onions", "Brown onions"),
            ("Red onions", "Sweeter variety of onion"),
            ("Garlic", "Fresh garlic cloves"),
            ("Carrots", "Orange root vegetables"),
            ("Potatoes", "UK white potatoes"),
            ("Tomatoes", "Fresh salad tomatoes"),
            ("Cherry tomatoes", "Small sweet tomatoes"),
            ("Mushrooms", "White closed cup mushrooms"),
            ("Spinach", "Fresh baby spinach leaves"),
            ("Peppers", "Bell peppers (mixed colours)"),

            # Meat & Protein
            ("Chicken breast", "Boneless, skinless chicken breast"),
            ("Minced beef", "Ground beef"),
            ("Bacon", "Back or streaky rashers"),
            ("Sausages", "Pork sausages"),
            ("Eggs", "Free-range chicken eggs"),
            ("Tuna", "Tinned in brine or oil"),
            ("Lentils", "Red or green lentils"),
            ("Chickpeas", "Tinned or dried"),
            ("Red kidney beans", "Common in chilli dishes"),

            # Grains & Pasta
            ("Rice", "Long grain or basmati"),
            ("Pasta", "Dried pasta shapes"),
            ("Spaghetti", "Classic long pasta"),
            ("Couscous", "Quick-cook grains"),
            ("Bread", "Sliced white or wholemeal loaf"),
            ("Wraps", "Tortilla wraps"),

            # Other
            ("Stock cubes", "Chicken or vegetable stock"),
            ("Honey", "Runny honey"),
            ("Lemon juice", "Fresh or bottled"),
            ("Yeast", "Dried active yeast"),
        ]

        count = 0
        for name, description in ingredients:
            obj, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'created_at': timezone.now(),
                    'updated_at': timezone.now()
                }
            )
            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {count} new common UK ingredients')
        )
