import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acholacakes.settings')
django.setup()

from store.models import AddOn

addons = [
    {'name': 'Extra Frosting', 'price': 5.00},
    {'name': 'Gold Sprinkles', 'price': 3.50},
    {'name': 'Edible Flowers', 'price': 7.00},
    {'name': 'Chocolate Drip', 'price': 4.00},
    {'name': 'Happy Birthday Topper', 'price': 10.00},
]

for addon_data in addons:
    addon, created = AddOn.objects.get_or_create(name=addon_data['name'], defaults={'price': addon_data['price']})
    if created:
        print(f"Created addon: {addon}")
    else:
        print(f"Addon already exists: {addon}")
