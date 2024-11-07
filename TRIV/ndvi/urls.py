from django.urls import path
from . import views

urlpatterns = [
    path('', views.ndvi, name='ndvi'),  # Existing HTTP route
]