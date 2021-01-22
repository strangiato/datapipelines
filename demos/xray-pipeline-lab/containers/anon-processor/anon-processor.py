import logging
import sys

from cloudevents.http import from_http

from flask import Flask, request

from flask_cors import CORS

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

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
