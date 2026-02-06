import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acholacakes.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product
from django.core.files.base import ContentFile

def create_data():
    # Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created (password: admin123)")
    else:
        print("Superuser 'admin' already exists")

    # Create Categories
    cat_birthday, _ = Category.objects.get_or_create(name='Birthday Cakes', slug='birthday-cakes')
    cat_wedding, _ = Category.objects.get_or_create(name='Wedding Cakes', slug='wedding-cakes')
    cat_cupcakes, _ = Category.objects.get_or_create(name='Cupcakes', slug='cupcakes')

    # Create Products
    if not Product.objects.filter(name='Chocolate Delight').exists():
        p1 = Product.objects.create(
            category=cat_birthday,
            name='Chocolate Delight',
            slug='chocolate-delight',
            description='Rich chocolate layer cake with fudge frosting.',
            ingredients='Flour, Sugar, Cocoa, Butter, Eggs, Milk.',
            size='8 inch (10-12 servings)',
            price=45.00,
            stock=10
        )
        print(f"Created Product: {p1.name}")

    if not Product.objects.filter(name='Vanilla Bean Dream').exists():
        p2 = Product.objects.create(
            category=cat_wedding,
            name='Vanilla Bean Dream',
            slug='vanilla-bean-dream',
            description='Elegant vanilla cake with buttercream.',
            ingredients='Flour, Sugar, Butter, Eggs, Vanilla Bean.',
            size='3 Tier',
            price=150.00,
            stock=2
        )
        print(f"Created Product: {p2.name}")

if __name__ == '__main__':
    create_data()
