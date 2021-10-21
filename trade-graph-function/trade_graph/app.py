import json
import os
from datetime import datetime

import yfinance as yf
import pytz

import boto3
from boto3.dynamodb.conditions import Key

from GraphUtil import GraphUtil

LONDON_TMZ = pytz.timezone('Europe/London')
TIME_PERIOD = '14d'
TIME_INTERVAL = '30m'


def get_dynamo_table(table_name):
    if 'AWS_KEY_ID' in os.environ:
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_KEY_SECRET'))
    else:
        session = boto3.Session()

    dynamodb = session.resource('dynamodb', region_name='us-east-1')

    return dynamodb.Table(table_name)


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


def get_account(account_id):
    table = get_dynamo_table('cb-mock-account')

    response = table.query(
        KeyConditionExpression=Key('account_id').eq(account_id),
    )

    return response['Items'][0]


def get_buys(transactions):
    return [d for d in transactions if d['operation'] == 'BUY']


def get_sells(transactions):
    return [d for d in transactions if d['operation'] == 'SELL']


def handler(event, context):
    print(event)  # Log the event

    if event['pathParameters']['account-id'] is None:
        print("ERROR: no query string param passed " + event['pathParameters'])

        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No account_id query string param was passed"
            }),
        }

    account_identifier = event['pathParameters']['account-id']  # Get account id from from query string

    # Get the account
    account = get_account(account_identifier)

    # Get the transactions
    transactions = get_transactions(account_id=account_identifier)

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
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Origin, X-Auth-Token",
            "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
        },
        "body": json.dumps({
            "message": figure.get_json()
        }),
    }
