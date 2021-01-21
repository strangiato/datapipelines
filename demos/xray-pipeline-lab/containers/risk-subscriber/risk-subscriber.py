import logging
import os
import sys

from kafka import KafkaConsumer

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

##############
#  Vars init #
##############

# kafka producer

kafka_server = os.environ["kafka_server"]
pneumonia_topic = os.environ["kafka_pneumonia_topic"]
try:
    consumer = KafkaConsumer(
        pneumonia_topic,
        bootstrap_servers=[kafka_server],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-group",
        value_deserializer=lambda x: loads(x.decode("utf-8")),
    )
except:
    logging.exception("Failed to connect to kafka_server", kafka_server)


# Launch Flask server
if __name__ == "__main__":
    for message in consumer:
        message = message.value
        logging.info(message)
