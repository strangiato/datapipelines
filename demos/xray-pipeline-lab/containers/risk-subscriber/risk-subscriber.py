import io
import logging
import os
import gc
import sys
from hashlib import blake2b
from io import BytesIO

import boto3
import numpy as np
import tensorflow as tf

from cloudevents.http import from_http
from kafka import KafkaConsumer
from flask import Flask, request
from flask_cors import CORS

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

##############
#  Vars init #
##############

# kafka producer

kafka_server = os.environ["kafka_server"]
pneumonia_topic = os.environ["kafka_pneumonia_topic"]
try:
    consumer = KafkaConsumer(pneumonia_topic, bootstrap_servers=[kafka_server])
except:
    logging.exception("Failed to connect to kafka_server", kafka_server)


# Launch Flask server
if __name__ == "__main__":
    for message in consumer:
        message = message.value
        logging.info(message)
