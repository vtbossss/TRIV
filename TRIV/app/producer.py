import requests
import json
from kafka import KafkaProducer
import time
import logging
from django.conf import settings

# Kafka configuration
from dotenv import load_dotenv
import os
import sys

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

# Graceful shutdown of Kafka producer
def shutdown_producer():
    logging.info("Shutting down producer...")
    producer.flush()  # Ensure all messages are sent
    producer.close()  # Close the producer

# Run the Kafka producer at a specific interval (every 12 hours)
try:
    while True:
        send_soil_data_to_kafka()
        
        # Calculate the next time to fetch data (12 hours from now)
        current_time = time.localtime()
        next_run = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday, 12, 0, 0, 0, 0, 0))  # Next 12:00 PM
        sleep_time = next_run - time.mktime(current_time)  # Time to sleep until next fetch
        
        # If we're past 12:00 PM, schedule for next day's 12:00 AM
        if sleep_time <= 0:
            next_run = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday + 1, 0, 0, 0, 0, 0, 0))
            sleep_time = next_run - time.mktime(current_time)
        
        logging.info(f"Sleeping for {sleep_time} seconds until next fetch.")
        time.sleep(5)  # Sleep until the next 12:00 PM or 12:00 AM
    
except KeyboardInterrupt:
    logging.info("Producer interrupted. Shutting down...")
    shutdown_producer()
    sys.exit(0)

except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
    shutdown_producer()
    sys.exit(1)
