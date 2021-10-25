import json
from AccountUtil import MockAccountUtil


def handler(event, context):
    print(json.dumps(event))  # Log the event
    print(context)  # Log the context

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Origin, X-Auth-Token",
            "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
        },
        "body": json.dumps({
            "data": MockAccountUtil.get_accounts()
        }),
    }
