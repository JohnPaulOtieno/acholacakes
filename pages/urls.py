from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policies/', views.policies, name='policies'),
    path('success/', views.success_view, name='success'),
]
