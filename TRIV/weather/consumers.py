import json
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
from channels.layers import get_channel_layer
import asyncio

KAFKA_TOPIC = 'weather_topic'
KAFKA_SERVER = 'localhost:9093'

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "weather_updates"

        # Join the weather updates group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Create Kafka consumer instance in background
        self._consume_task = asyncio.create_task(self.consume_kafka_messages())

    async def disconnect(self, close_code):
        # Close the Kafka consumer and WebSocket connection on disconnect
        if hasattr(self, '_consume_task'):
            self._consume_task.cancel()

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def consume_kafka_messages(self):
        """ Consume Kafka messages and push them to WebSocket. """
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            group_id='django-group',
            auto_offset_reset='latest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        channel_layer = get_channel_layer()

        # Continuously consume messages from Kafka
        for message in consumer:
            weather_data = message.value
            # Send weather data to WebSocket group
            await channel_layer.group_send(
                'weather_updates',
                {
                    'type': 'weather_update',
                    'weather_data': weather_data
                }
            )

    # Receive message from WebSocket (not used here, but could be added for two-way communication)
    async def receive(self, text_data):
        pass

    # Broadcast weather data to WebSocket clients
    async def weather_update(self, event):
        weather_data = event['weather_data']
        await self.send(text_data=json.dumps({
            'weather': weather_data
        }))
