import json

from CommonsUtil import CommonsUtil, MockAccountUtil


def handler(event, context):
    print(json.dumps(event))  # Log the event

    # Make sure user_id is passed and is authorized for the account
    try:
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
    except AttributeError:
        user_id = None

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": MockAccountUtil.get_accounts(user_id)
        }),
    }
