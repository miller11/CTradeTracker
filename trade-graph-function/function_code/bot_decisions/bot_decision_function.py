import json
from datetime import datetime, timedelta
from CommonsUtil import CommonsUtil
from boto3.dynamodb.conditions import Key
import time


def get_bot_decisions(account_identifier):
    table = CommonsUtil.get_dynamo_table('cb-bot-decision')

    query_time = datetime.today() - timedelta(days=14)

    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_identifier) & Key('timestamp').gt(
            int(query_time.timestamp()))
    )

    for item in response['Items']:
        item['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp']))

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
        return CommonsUtil.NO_ACCOUNT_RESPONSE

    # Make sure user_id is passed and is authorized for the account
    try:
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
    except AttributeError:
        user_id = None

    # Check authorized
    if user_id is None or not CommonsUtil.is_authorized_account(user_id, account_identifier):
        print("ERROR: no authenticated user or unauthorized: " + event['requestContext'])
        return CommonsUtil.UNAUTHORIZED_RESPONSE

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": get_bot_decisions(account_identifier)
        })
    }
