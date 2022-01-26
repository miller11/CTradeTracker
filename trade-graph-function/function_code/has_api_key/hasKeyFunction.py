import simplejson as json
from botocore.exceptions import ClientError
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event

    key_saved = False

    # Make sure user_id is passed and is authorized for the account
    try:
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
    except AttributeError:
        user_id = None

    # Check to make sure that the body is passed
    try:
        key = CommonsUtil.get_ssm_param(f"/ic-miller/trader-bot/{user_id}/cb-access-key")

        if key is not None:
            key_saved = True

    except (ClientError, AttributeError, ValueError) as e:
        print(f"ERROR: unable to get key for user: {user_id}. {str(e)}")

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": {'keySaved': key_saved}
        }),
    }
