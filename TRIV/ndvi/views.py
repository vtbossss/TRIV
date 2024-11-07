from django.shortcuts import render

# Create your views here.
def ndvi(request):
    return render(request,'ndvi.html')