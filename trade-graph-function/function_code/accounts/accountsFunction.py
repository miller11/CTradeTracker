import json

from CommonsUtil import CommonsUtil, MockAccountUtil


def handler(event, context):
    print(json.dumps(event))  # Log the event

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": MockAccountUtil.get_accounts()
        }),
    }
