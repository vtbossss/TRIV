import json
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
from channels.layers import get_channel_layer
import asyncio
import threading

KAFKA_TOPIC = 'weather_topic'
KAFKA_SERVER = 'kafka:9092'

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "weather_updates"

        # Join the weather updates group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Create Kafka consumer instance in the background
        # Run Kafka consumer in a separate thread to avoid blocking the event loop
        self._consume_thread = threading.Thread(target=self.consume_kafka_messages)
        self._consume_thread.daemon = True  # Ensure the thread is terminated when the application shuts down
        self._consume_thread.start()

    async def disconnect(self, close_code):
        # Cancel the Kafka consumer thread when WebSocket disconnects
        if hasattr(self, '_consume_thread'):
            self._consume_thread.join()  # Ensure the thread stops before exiting

        # Remove the WebSocket from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def consume_kafka_messages(self):
        """ Consume Kafka messages and send them to WebSocket. """
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            group_id='django-group',
            auto_offset_reset='latest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        # Loop to consume Kafka messages
        for message in consumer:
            weather_data = message.value
            # Send the weather data to the WebSocket group asynchronously
            asyncio.run(self.send_weather_to_websocket(weather_data))

    async def send_weather_to_websocket(self, weather_data):
        """ Send weather data to the WebSocket client. """
        # Send the weather data to the WebSocket group
        await self.channel_layer.group_send(
            self.group_name,  # Broadcast to all connected WebSocket clients
            {
                'type': 'weather_update',
                'weather_data': weather_data
            }
        )

    # This method is used to send the message to the WebSocket client
    async def weather_update(self, event):
        weather_data = event['weather_data']
        # Send the weather data to the WebSocket client
        await self.send(text_data=json.dumps({
            'weather': weather_data
        }))
