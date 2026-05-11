import json


def handler(event, context):
    payload = {
        "summary": {},
        "map_data": [],
        "news_feed": [],
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(payload),
    }
