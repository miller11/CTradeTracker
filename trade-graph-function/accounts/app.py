import json

from boto3.dynamodb.conditions import Key
from datetime import datetime
import pytz
from AccountUtil import MockAccountUtil, get_dynamo_table


LONDON_TMZ = pytz.timezone('Europe/London')


HEADERS = {
    "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
    "Access-Control-Allow-Headers": "Content-Type, Authorization, Origin, X-Auth-Token",
    "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
}


def _normalize_timestamp(epoch_time):
    return LONDON_TMZ.localize(datetime.fromtimestamp(epoch_time)).strftime('%Y-%m-%d %H:%M:%S')


def get_transactions(account_id):
    table = get_dynamo_table('cb-bot-transaction')

    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id)
    )

    transaction_list = response['Items']

    for transaction in transaction_list:
        transaction['timestamp'] = _normalize_timestamp(transaction['timestamp'])

    return transaction_list


def accounts_handler(event, context):
    print(json.dumps(event))  # Log the event

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({
            "data": MockAccountUtil.get_accounts()
        }),
    }


def transactions_handler(event, context):
    print(json.dumps(event))  # Log the event
    print(event['requestContext']['accountId'])  # Log the account id

    # todo throw 403 if no user account

    if event['pathParameters']['account-id'] is None:
        print("ERROR: no query string param passed " + event['pathParameters'])

        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No account_id query string param was passed"
            }),
        }

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({
            "data": get_transactions(event['pathParameters']['account-id'])
        }),
    }
