import json

import yfinance as yf
from boto3.dynamodb.conditions import Key

from GraphUtil import GraphUtil
from CommonsUtil import CommonsUtil

GRAPH_DAYS = 14
TIME_PERIOD = str(GRAPH_DAYS) + 'd'  # This will turn out as 14d
TIME_INTERVAL = '30m'


def get_account(account_id):
    table = CommonsUtil.get_dynamo_table(CommonsUtil.ACCOUNT_TABLE)

    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id),
    )

    return response['Items'][0]


def get_buys(transactions):
    return [d for d in transactions if d['operation'] == 'BUY']


def get_sells(transactions):
    return [d for d in transactions if d['operation'] == 'SELL']


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

    # Get the account
    account = get_account(account_identifier)

    # Get the transactions
    transactions = CommonsUtil.get_transactions(account_id=account_identifier)

    # Importing market data
    data = yf.download(tickers=account['currency'] + '-USD', period=TIME_PERIOD, interval=TIME_INTERVAL)

    # Define Graph Util
    figure = GraphUtil(data)

    # Add plot lines for the buys
    for buy in get_buys(transactions):
        figure.add_account_buy(str(buy['timestamp']))

    # Add plot lines for the sells
    for sell in get_sells(transactions):
        figure.add_account_sell(str(sell['timestamp']))

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "message": figure.get_json()
        }),
    }
