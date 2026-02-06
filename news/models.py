from django.db import models
from django.urls import reverse


class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='news/images/')
    tags = models.CharField(max_length=255, default='CELEBRATION', help_text="Comma-separated tags")
    excerpt = models.TextField(help_text="Short summary for the homepage")
    content = models.TextField(blank=True, help_text="Full article content (optional for now)")
    published_date = models.DateField()
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Link a product to allow ordering from this news post"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[self.slug])
