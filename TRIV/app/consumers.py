import json
import asyncio
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

KAFKA_TOPIC = 'soil_data_topic'
KAFKA_SERVER = 'kafka:9092'


class AgroDataConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_consumer = False  # Flag to stop the Kafka consumer gracefully
        self._consume_task = None    # To track the background Kafka consumer task
        self.consumer = None         # Kafka consumer instance
        self.group_name = "soil_data_group"  # Initialize the group_name

    async def connect(self):
        """
        Handle WebSocket connection. Initialize Kafka consumer and start background task.
        """
        # Accept the WebSocket connection
        await self.accept()

        try:
            # Initialize Kafka consumer only once
            if not self.consumer:
                self.consumer = KafkaConsumer(
                    KAFKA_TOPIC,
                    bootstrap_servers=KAFKA_SERVER,
                    group_id=None,  # Stateless consumption
                    auto_offset_reset='latest',  # Read only new messages
                    session_timeout_ms=45000,  # 45 seconds session timeout
                    heartbeat_interval_ms=15000,  # Heartbeat every 15 seconds
                    max_poll_interval_ms=600000  # Allow up to 10 minutes for processing
                )

            # Start the background task to consume Kafka messages
            if not self._consume_task or self._consume_task.done():
                self._consume_task = asyncio.create_task(self.consume_kafka_messages())

        except KafkaError as e:
            print(f"Error initializing Kafka consumer: {e}")
            await self.close()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection. Properly clean up Kafka consumer and tasks.
        """
        # Signal the consumer task to stop
        self._stop_consumer = True

        # Cancel Kafka consumer task if it is still running
        if self._consume_task and not self._consume_task.cancelled():
            self._consume_task.cancel()
            try:
                await self._consume_task
            except asyncio.CancelledError:
                pass

        # Close Kafka consumer connection gracefully
        if self.consumer:
            self.consumer.close()

        # Ensure WebSocket group removal
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handle messages from the frontend (if needed).
        """
        pass

    async def consume_kafka_messages(self):
        """
        Consume Kafka messages in a background thread and send them to the WebSocket.
        """
        try:
            while not self._stop_consumer:
                # Poll Kafka for new messages (this runs in a background thread to avoid blocking)
                messages = await asyncio.to_thread(self.consumer.poll, timeout_ms=1000)

                for _, messages_partition in messages.items():
                    for msg in messages_partition:
                        if self._stop_consumer:
                            return

                        try:
                            data = json.loads(msg.value.decode('utf-8'))
                            print("Received data from Kafka:", data)

                            # Send data to the WebSocket client
                            await self.send(text_data=json.dumps({'data': data}))

                        except (json.JSONDecodeError, UnicodeDecodeError) as e:
                            print(f"Error decoding message: {e}")
                        except Exception as e:
                            print(f"Unexpected error processing message: {e}")

                # Throttle polling to reduce resource usage
                await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            print("Kafka consumer task canceled.")
        except KafkaError as e:
            print(f"Kafka error: {e}")
        finally:
            # Close Kafka consumer gracefully
            if self.consumer:
                self.consumer.close()
