from rest_framework.response import Response
from rest_framework.decorators import api_view
from .producer import fetch_and_send_weather
from django.shortcuts import render# Import the function

@api_view(['GET'])
def weather_by_coordinates(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')

    if not lat or not lon:
        return Response({'error': 'Latitude and Longitude are required.'}, status=400)

    try:
        lat, lon = float(lat), float(lon)
    except ValueError:
        return Response({'error': 'Invalid latitude or longitude.'}, status=400)

    # Fetch and send weather data
    fetch_and_send_weather(lat, lon)

    # Return success message
    return Response({"message": "Weather data fetch started."})

def weather_test(request):
    return render(request,'weathertest.html')