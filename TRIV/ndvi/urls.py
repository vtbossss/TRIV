from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.ndvi_history, name='ndvi_history'),  # Existing HTTP route
]