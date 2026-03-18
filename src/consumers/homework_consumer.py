import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from kafka import KafkaConsumer

sys.path.insert(0, str(Path(__file__).parent.parent / 'producers'))
from homework_producer import green_ride_deserializer

load_dotenv()

count =  0

def main():
    redpanda_port = os.getenv('REDPANDA_PORT', '9092')
    consumer = KafkaConsumer(
        'green-trips',
        bootstrap_servers=[f'localhost:{redpanda_port}'],
        auto_offset_reset='earliest',
        group_id='green-rides-counter',
        value_deserializer=green_ride_deserializer
    )

    global count

    for message in consumer:
        ride = message.value
        if ride.trip_distance > 5:
            count += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nThe consumer was down!")

    print(f'The are {count} trips with trip_distance greater than 5.0 kilometers')
