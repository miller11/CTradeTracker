import simplejson as json
import boto3
from CommonsUtil import CommonsUtil


def put_param(client, name, value):
    client.put_parameter(Name=name, Value=value, Overwrite=True, Type='SecureString')


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event

    # Make sure user_id is passed and is authorized for the account
    try:
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
    except AttributeError:
        print("ERROR: user not authenticated ")
        return CommonsUtil.error_message_response("User not authenticated")

    client = boto3.client('ssm')  # Establish the ssm client

    # Check to make sure that the body is passed
    try:
        body = json.loads(event['body'])
        put_param(client, f"/ic-miller/trader-bot/{user_id}/cb-access-key", body['accessKey'])
        put_param(client, f"/ic-miller/trader-bot/{user_id}/cb-access-passphrase", body['passphrase'])
        put_param(client, f"/ic-miller/trader-bot/{user_id}/cb-access-secret", body['secret'])
    except AttributeError:
        print("ERROR: no body with new account passed " + event['body'])
        return CommonsUtil.error_message_response("Message body did not contain required information")

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": "API secret saved successfully."
        }),
    }
