from django.shortcuts import render, get_object_or_404
from .models import NewsPost


def news_detail(request, slug):
    """Display a single news post with full content."""
    post = get_object_or_404(NewsPost, slug=slug, is_active=True)
    return render(request, 'news/news_detail.html', {'post': post})
