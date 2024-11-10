from rest_framework.response import Response
from rest_framework.decorators import api_view

from .producer import send_weather_to_kafka,fetch_and_send_weather
from django.shortcuts import render
@api_view(['GET'])
def weather_by_coordinates(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')

    if not lat or not lon:
        return Response({'error': 'Latitude and Longitude are required.'}, status=400)

    # Fetch weather data from Agromonitoring API
    weather_data = fetch_and_send_weather(lat, lon)

    if "error" in weather_data:
        return Response({'error': weather_data['error']}, status=400)

    # Send the fetched weather data to Kafka
    send_weather_to_kafka(weather_data)

    # Return the weather data as a response (without storing it)
    return Response(weather_data)

def weather_test(request):
    return render(request,"weathertest.html")