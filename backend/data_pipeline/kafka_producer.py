import pandas as pd
import json
import time
from kafka import KafkaProducer

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def stream_interactions(file_path, topic="user_interactions", delay=0.01):
    """
    Reads interactions from a CSV file and streams them to a Kafka topic.
    A delay (in seconds) is added between events to simulate real-time streaming.
    """
    interactions_df = pd.read_csv(file_path)
    for _, row in interactions_df.iterrows():
        event = row.to_dict()
        producer.send(topic, value=event)
        time.sleep(delay)
    producer.flush()
    print("Finished streaming interactions.")

if __name__ == "__main__":
    # Adjust the file path if necessary
    stream_interactions("../data/large_interactions.csv")
