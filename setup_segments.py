import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acholacakes.settings')
django.setup()

from store.models import Category, Product

# 1. Create Categories
wedding_cat, _ = Category.objects.get_or_create(name="Wedding Cakes", defaults={'slug': 'wedding-cakes'})
custom_cat, _ = Category.objects.get_or_create(name="Custom Cakes", defaults={'slug': 'custom-cakes'})

print(f"Categories: {wedding_cat}, {custom_cat}")

# 2. Mark Bestsellers (Randomly select 3 existing products)
all_products = list(Product.objects.all())
if all_products:
    bestsellers = random.sample(all_products, min(len(all_products), 3))
    for p in bestsellers:
        p.is_bestseller = True
        p.save()
        print(f"Marked as Bestseller: {p.name}")

# 3. Assign some products to Wedding and Custom if they are empty
# (Just for demo purposes, moving some existing products if needed)
# In a real scenario, you'd create new products.
# We will just ensure we have at least one in specific cats if possible, or create placeholders.

if not Product.objects.filter(category=wedding_cat).exists():
    Product.objects.create(
        category=wedding_cat,
        name="Elegant Rose Wedding Cake",
        slug="elegant-rose-wedding-cake",
        description="Three-tier white cake with edible roses.",
        price=350.00,
        image='products/images/wedding_placeholder.jpg' # Assumption: placeholder exists or will be broken image
    )
    print("Created placeholder Wedding Cake")

if not Product.objects.filter(category=custom_cat).exists():
    Product.objects.create(
        category=custom_cat,
        name="Superhero Theme Cake",
        slug="superhero-theme-cake",
        description="Custom design for your little hero.",
        price=120.00,
        image='products/images/custom_placeholder.jpg'
    )
    print("Created placeholder Custom Cake")
