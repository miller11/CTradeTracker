import json
from datetime import datetime, timedelta
from CommonsUtil import CommonsUtil
from boto3.dynamodb.conditions import Key
import time


def get_bot_decisions(account_identifier, days_back):
    table = CommonsUtil.get_dynamo_table(CommonsUtil.DECISIONS_TABLE)

    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_identifier) & Key('timestamp').gt(
            CommonsUtil.get_time_since_epoch(days_back))
    )

    for item in response['Items']:
        item['timestamp'] = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(item['timestamp'] / 1000))

    return response['Items']


def handler(event, context):
    print(json.dumps(event))  # Log the event

    # Check to make sure account-id is passed
    try:
        account_identifier = event['pathParameters']['account-id']  # Get account id from from query string
    except AttributeError:
        account_identifier = None

    if account_identifier is None:
        print("ERROR: no query string param passed " + event['pathParameters'])
        return CommonsUtil.error_message_response("No account_id query string param was passed")

    # Make sure user_id is passed and is authorized for the account
    try:
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
    except AttributeError:
        user_id = None

    # Check authorized
    if user_id is None or not CommonsUtil.is_authorized_account(user_id, account_identifier):
        print("ERROR: no authenticated user or unauthorized: " + event['requestContext'])
        return CommonsUtil.UNAUTHORIZED_RESPONSE

    # Check days back
    try:
        days_back = int(event['queryStringParameters']['days_back'])
    except AttributeError:
        days_back = 14

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": get_bot_decisions(account_identifier, days_back)
        })
    }
