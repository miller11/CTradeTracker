import simplejson as json
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event

    # Make sure user_id is passed and is authorized for the account
    try:
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
    except AttributeError:
        print("ERROR: user not authenticated ")
        return CommonsUtil.error_message_response("User not authenticated")

    auth_client = CommonsUtil.get_cbp_client(user_id)

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": auth_client.get_accounts()
        }),
    }
