import logging
import os
import sys

import boto3

from cloudevents.http import from_http

from flask import Flask, request

from flask_cors import CORS

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

##############
# Vars init #
##############
# Object storage
access_key = os.environ["AWS_ACCESS_KEY_ID"]
secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
service_point = os.environ["service_point"]
s3client = boto3.client(
    "s3",
    "us-east-1",
    endpoint_url=service_point,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    use_ssl=True if "https" in service_point else False,
)

# Bucket base name
bucket_base_name = os.environ["bucket-base-name"]

# Helper database
db_user = os.environ["database-user"]
db_password = os.environ["database-password"]
db_host = os.environ["database-host"]
db_db = os.environ["database-db"]


########
# Code #
########
# Main Flask app
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def home():
    # Retrieve the CloudEvent
    event = from_http(request.headers, request.get_data())

    # Process the event
    process_event(event.data)

    return "", 204


def process_event(data):
    """Main function to process data received by the container image."""

    logging.info(data)
    try:
        # Retrieve event info
        extracted_data = extract_data(data)
        bucket_eventName = extracted_data["bucket_eventName"]
        bucket_name = extracted_data["bucket_name"]
        img_key = extracted_data["bucket_object"]
        # img_name = img_key.split("/")[-1]
        logging.info(bucket_eventName + " " + bucket_name + " " + img_key)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


def extract_data(data):
    logging.info("extract_data")
    record = data["Records"][0]
    bucket_eventName = record["eventName"]
    bucket_name = record["s3"]["bucket"]["name"]
    bucket_object = record["s3"]["object"]["key"]
    data_out = {
        "bucket_eventName": bucket_eventName,
        "bucket_name": bucket_name,
        "bucket_object": bucket_object,
    }
    return data_out


# Launch Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0")  # noqa: S104
