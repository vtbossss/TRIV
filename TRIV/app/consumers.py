import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
import time

KAFKA_TOPIC = 'soil_data_topic'
KAFKA_SERVER = 'localhost:9093'

class AgroDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Create Kafka consumer
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            group_id='django-group',
            auto_offset_reset='latest'
        )

        # Start a background task to consume Kafka messages
        self._consume_task = asyncio.create_task(self.consume_kafka_messages())

    async def disconnect(self, close_code):
        # Close the Kafka consumer on WebSocket disconnect
        self.consumer.close()
        if hasattr(self, '_consume_task'):
            self._consume_task.cancel()

    async def receive(self, text_data):
        # This function can be used to handle messages from the frontend, if needed
        pass

    async def consume_kafka_messages(self):
        # Use asyncio.to_thread to run the blocking Kafka poll in a background thread
        while True:
            # Poll Kafka for a message using to_thread to avoid blocking the asyncio event loop
            messages = await asyncio.to_thread(self.consumer.poll, timeout_ms=1000)  # Poll for a message with a 1 second timeout

            for _, messages_partition in messages.items():  # Iterate over the messages in each partition
                for msg in messages_partition:
                    # Extract data from the message
                    try:
                        data = json.loads(msg.value.decode('utf-8'))
                        
                        # Print the data to the console for debugging
                        print("Received data from Kafka:", data)

                        # Send the data to WebSocket client (optional, if needed)
                        await self.send(text_data=json.dumps({
                            'data': data
                        }))
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        continue
