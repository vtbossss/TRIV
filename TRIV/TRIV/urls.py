from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin panel route
    path('', include('app.urls')),
    path('ndvi/', include('ndvi.urls')),# Include the app's URL configurations
]
