from django.contrib import admin
from .models import NewsPost

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_active']
    list_filter = ['is_active', 'published_date']
    search_fields = ['title', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
