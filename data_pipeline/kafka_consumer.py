import json
import redis
from kafka import KafkaConsumer

# Setup Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Setup Kafka consumer to listen to the 'user_interactions' topic
consumer = KafkaConsumer(
    'user_interactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # For production, you might set this to 'latest'
    enable_auto_commit=True,
    group_id='recommendation_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def process_message(message):
    """
    Process each incoming Kafka message:
      - Extracts the user_id.
      - Stores the event in Redis under a key associated with the user.
    """
    user_id = message.get("user_id")
    if user_id:
        redis_key = f"session:{user_id}"
        # Append event to the Redis list for this user
        redis_client.rpush(redis_key, json.dumps(message))
        # Set an expiration time of 1 hour for session data (optional)
        redis_client.expire(redis_key, 3600)
        print(f"Stored event for user {user_id}")

def consume_messages():
    print("Starting Kafka consumer...")
    for msg in consumer:
        message = msg.value
        process_message(message)

if __name__ == "__main__":
    consume_messages()
