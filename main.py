import json
from google.cloud import pubsub_v1
from datetime import datetime

# initialize once (important for performance)
publisher = pubsub_v1.PublisherClient()

PROJECT_ID = "alubee-prod"
TOPIC_ID = "production-loader-topic"
TOPIC_PATH = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def publish_iot(request):
    """
    HTTP Cloud Function
    Receives JSON and publishes to Pub/Sub
    """

    try:
        # get JSON body
        request_json = request.get_json()

        if request_json is None:
            return {"error": "No JSON received"}, 400

        # add server timestamp (VERY IMPORTANT for BigQuery ordering)
        request_json["event_time"] = datetime.utcnow().isoformat()

        # convert to bytes
        data = json.dumps(request_json).encode("utf-8")

        # publish
        future = publisher.publish(TOPIC_PATH, data=data)
        message_id = future.result()

        return {
            "status": "success",
            "message_id": message_id,
            "received": request_json
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500