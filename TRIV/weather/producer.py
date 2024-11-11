import time
import requests
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os
import signal
import sys
import threading  # To run the periodic task in a separate thread
from .consumers import WeatherConsumer  # If you want to integrate the consumer class

load_dotenv()

# Kafka configuration
KAFKA_BROKER = 'localhost:9093'  # Your Kafka broker
KAFKA_TOPIC = 'weather_topic'    # Kafka topic to send data
API_KEY = os.getenv('API_KEY', 'default_api_key')  # Your API key

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_weather_to_kafka(weather_data):
    """
    Sends the weather data to Kafka topic for further consumption.
    """
    producer.send(KAFKA_TOPIC, weather_data)
    producer.flush()  # Ensure data is sent before closing
    print("Weather data sent to Kafka.")

def fetch_weather_once(LAT, LON):
    """
    Fetches weather data once for a specific lat, lon, and sends it to Kafka.
    """
    # Fetch the weather data from Agromonitoring API
    url = f'https://api.agromonitoring.com/agro/1.0/weather?lat={LAT}&lon={LON}&appid={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        print("Fetched weather data once.")
        send_weather_to_kafka(weather_data)
        return weather_data
    else:
        print(f"Failed to fetch weather data: {response.status_code}")
        return {"error": "Failed to fetch data"}

def fetch_and_send_weather_periodically(LAT, LON):
    """
    Fetches weather data at regular intervals and sends it to Kafka.
    """
    while True:
        # Fetch the weather data from Agromonitoring API
        url = f'https://api.agromonitoring.com/agro/1.0/weather?lat={LAT}&lon={LON}&appid={API_KEY}'
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()
            print("Fetched weather data periodically.")
            # Send the weather data to Kafka
            send_weather_to_kafka(weather_data)
        else:
            print(f"Failed to fetch weather data: {response.status_code}")
        
        # Wait for the specified interval (e.g., 1 minute) before fetching again
        time.sleep(60)  # Sleep for 1 minute (adjust as necessary)

def graceful_shutdown(signal, frame):
    """
    Handles graceful shutdown on keyboard interrupt.
    """
    print("\nGracefully shutting down...")
    producer.close()  # Close Kafka producer
    print("Kafka producer closed.")
    sys.exit(0)  # Exit the program

def start_periodic_fetching(LAT, LON):
    """
    Starts the periodic fetching in a separate thread so that the main thread is not blocked.
    """
    periodic_thread = threading.Thread(target=fetch_and_send_weather_periodically, args=(LAT, LON))
    periodic_thread.daemon = True  # Ensure the thread ends when the program exits
    periodic_thread.start()

def fetch_and_send_weather(lat, lon):
    """
    This function will be called in the Django view to fetch and send the weather data.
    """
    # Fetch weather once and then start periodic fetching
    fetch_weather_once(lat, lon)
    start_periodic_fetching(lat, lon)

