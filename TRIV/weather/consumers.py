import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from channels.layers import get_channel_layer

KAFKA_TOPIC = 'weather_topic'
KAFKA_SERVER = 'kafka:9092'

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handle WebSocket connection. Join the group and start consuming Kafka messages.
        """
        self.group_name = "weather_updates"

        # Add WebSocket to the weather updates group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Create Kafka consumer and start background task
        try:
            self.consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_SERVER,
                group_id=None,  # No group ID for stateless consumption
                auto_offset_reset='latest',  # Read only new messages
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                session_timeout_ms=45000,    # 45 seconds session timeout
                heartbeat_interval_ms=15000,  # Heartbeat every 15 seconds
                max_poll_interval_ms=600000  # Allow up to 10 minutes for processing
            )

            # Start consuming Kafka messages in a background task
            self._consume_task = asyncio.create_task(self.consume_kafka_messages())
        except KafkaError as e:
            await self.close()  # Close the WebSocket if Kafka initialization fails
            print(f"Error initializing Kafka consumer: {e}")

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection. Remove from group and clean up Kafka consumer.
        """
        # Stop Kafka consumer task
        if hasattr(self, '_consume_task') and not self._consume_task.cancelled():
            self._consume_task.cancel()
            try:
                await self._consume_task
            except asyncio.CancelledError:
                pass

        # Close Kafka consumer
        if hasattr(self, 'consumer'):
            self.consumer.close()

        # Remove WebSocket from the weather updates group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def consume_kafka_messages(self):
        """
        Consume Kafka messages asynchronously and send them to the WebSocket group.
        """
        try:
            while True:
                # Poll Kafka for messages (in a background thread to avoid blocking)
                messages = await asyncio.to_thread(self.consumer.poll, timeout_ms=1000)

                for _, messages_partition in messages.items():
                    for msg in messages_partition:
                        try:
                            # Extract and send weather data
                            weather_data = msg.value
                            print("Received weather data:", weather_data)

                            # Send to WebSocket group
                            await self.channel_layer.group_send(
                                self.group_name,
                                {
                                    'type': 'weather_update',
                                    'weather_data': weather_data
                                }
                            )
                        except (json.JSONDecodeError, UnicodeDecodeError) as e:
                            print(f"Error decoding message: {e}")
                        except Exception as e:
                            print(f"Unexpected error processing message: {e}")
        except asyncio.CancelledError:
            print("Kafka consumer task canceled.")
        except KafkaError as e:
            print(f"Kafka error: {e}")
        finally:
            self.consumer.close()

    async def weather_update(self, event):
        """
        Handle messages broadcast to the WebSocket group.
        """
        weather_data = event['weather_data']
        await self.send(text_data=json.dumps({
            'weather': weather_data
        }))
