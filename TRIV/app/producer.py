import requests
import json
from kafka import KafkaProducer
import time
import logging
from django.conf import settings

# Kafka configuration
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'default_topic')  # Use 'default_topic' if not found
KAFKA_SERVER = os.getenv('KAFKA_SERVER', 'localhost:9093')
API_KEY = os.getenv('API_KEY', 'default_api_key')
POLYGON_ID = os.getenv('POLYGON_ID', 'default_polygon_id')
# Set up logging
logging.basicConfig(level=logging.INFO)

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Function to fetch soil data from Agro Monitoring API
def fetch_soil_data():
    url = f'http://api.agromonitoring.com/agro/1.0/soil?polyid={POLYGON_ID}&appid={API_KEY}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {e}")
        return None

# Function to send soil data to Kafka
def send_soil_data_to_kafka():
    soil_data = fetch_soil_data()
    
    if soil_data:
        # Prepare the message to send to Kafka
        message = {
            'timestamp': time.time(),  # current time as timestamp
            'data': soil_data  # data fetched from API
        }
        
        try:
            # Send the data to Kafka topic
            producer.send(KAFKA_TOPIC, value=message)
            producer.flush()  # Ensure the message is sent immediately
            logging.info(f"Sent data to Kafka: {message}")
        except Exception as e:
            logging.error(f"Failed to send data to Kafka: {e}")
    else:
        logging.error("No data received from the API.")

# Run the Kafka producer every 12 hours (since soil data is updated twice a day)
while True:
    send_soil_data_to_kafka()
    time.sleep(1)  # Wait for 12 hours before fetching new data
