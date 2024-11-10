import time
import requests
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os
import signal
import sys
import argparse  # To parse command-line arguments for lat and lon

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

def fetch_and_send_weather(LAT, LON):
    """
    Fetches weather data at regular intervals and sends it to Kafka.
    """
    while True:
        # Fetch the weather data from Agromonitoring API
        url = f'https://api.agromonitoring.com/agro/1.0/weather?lat={LAT}&lon={LON}&appid={API_KEY}'
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()
            print("Fetched weather data.")
            # Send the weather data to Kafka
            send_weather_to_kafka(weather_data)
        else:
            print(f"Failed to fetch weather data: {response.status_code}")
        
        # Wait for a specified interval (e.g., 10 minutes)
        print("Waiting for the next fetch...")
        time.sleep(60)  # Sleep for 1 minute

def graceful_shutdown(signal, frame):
    """
    Handles graceful shutdown on keyboard interrupt.
    """
    print("\nGracefully shutting down...")
    producer.close()  # Close Kafka producer
    print("Kafka producer closed.")
    sys.exit(0)  # Exit the program

if __name__ == "__main__":
    # Register the signal handler for graceful shutdown on SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, graceful_shutdown)

    # Parse command-line arguments for lat and lon
    parser = argparse.ArgumentParser(description="Fetch and send weather data to Kafka.")
    parser.add_argument('--lat', type=float, required=True, help="Latitude of the location")
    parser.add_argument('--lon', type=float, required=True, help="Longitude of the location")
    args = parser.parse_args()

    # Run the weather fetching and sending process with dynamic lat and lon
    fetch_and_send_weather(args.lat, args.lon)
