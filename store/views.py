from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    query = request.GET.get('query')
    
    # Segment Data
    bestsellers = None
    wedding_cakes = None
    custom_cakes = None

    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        )
    elif not category_slug:
        # Only show segments on the main homepage (no category selected, no search)
        bestsellers = Product.objects.filter(is_active=True, is_bestseller=True)[:4]
        wedding_cakes = Product.objects.filter(is_active=True, category__name="Wedding Cakes")[:4]
        custom_cakes = Product.objects.filter(is_active=True, category__name="Custom Cakes")[:4]

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Fetch latest news post for homepage
    from news.models import NewsPost
    latest_news = NewsPost.objects.filter(is_active=True).first() if not category_slug else None

    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'bestsellers': bestsellers,
        'wedding_cakes': wedding_cakes,
        'custom_cakes': custom_cakes,
        'latest_news': latest_news,
    })

from cart.forms import CartAddProductForm

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })
