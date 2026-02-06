from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('<slug:slug>/', views.news_detail, name='news_detail'),
]
