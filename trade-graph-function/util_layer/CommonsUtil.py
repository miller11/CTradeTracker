from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
import os
import boto3
import pytz
import json
import time


LONDON_TMZ = pytz.timezone('Europe/London')


class CommonsUtil:
    ACCOUNT_TABLE = 'cb-mock-account'
    DECISIONS_TABLE = 'cbp-bot-decision'
    TRANSACTION_TABLE = 'cbp-bot-transaction'

    HEADERS = {
        "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Origin, X-Auth-Token",
        "Access-Control-Allow-Methods": "GET, POST, PATCH, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
    }

    NO_ACCOUNT_RESPONSE = {
        "statusCode": 404,
        "headers": HEADERS,
        "body": json.dumps({
            "message": "No account_id query string param was passed"
        }),
    }

    UNAUTHORIZED_RESPONSE = {
        "statusCode": 403,
        "headers": HEADERS,
        "body": json.dumps({
            "message": "User is not authorized to access that account"
        }),
    }

    @staticmethod
    def get_ssm_param(param_path):
        ssm = boto3.client('ssm', region_name='us-east-1')
        return ssm.get_parameter(Name=param_path, WithDecryption=True)['Parameter']['Value']

    @staticmethod
    def get_cb_client():
        # todo this won't work in AWS
        return None

    @staticmethod
    def get_dynamo_table(table_name):
        if 'AWS_KEY_ID' in os.environ:
            session = boto3.Session(
                aws_access_key_id=os.getenv('AWS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_KEY_SECRET'))
        else:
            session = boto3.Session()

        dynamodb = session.resource('dynamodb', region_name='us-east-1')

        return dynamodb.Table(table_name)

    @staticmethod
    def _normalize_timestamp(epoch_time):
        return LONDON_TMZ.localize(datetime.fromtimestamp(epoch_time)).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_transactions(account_id, days_back=14):
        table = CommonsUtil.get_dynamo_table('cb-bot-transaction')
        query_time = datetime.today() - timedelta(days=days_back)

        response = table.query(
            KeyConditionExpression=Key('account_id').eq(account_id) & Key('timestamp').gt(
                int(query_time.timestamp()))
        )

        transaction_list = response['Items']

        for transaction in transaction_list:
            transaction['timestamp'] = CommonsUtil._normalize_timestamp(transaction['timestamp'])

        return transaction_list

    @staticmethod
    def is_authorized_account(user_id, account_id):
        table = CommonsUtil.get_dynamo_table('cb_user_accounts')

        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )

        cached_accounts = response['Items']

        if any(cached_account['account_id'] == account_id for cached_account in cached_accounts):
            return True

        accounts = MockAccountUtil.get_accounts()

        has_match = False

        for account in accounts:
            if account['account_id'] == account_id:
                has_match = True

            if not any(cached_account['account_id'] == account_id for cached_account in cached_accounts):
                cached_account = {
                    'user_id': user_id,
                    'account_id': account['account_id'],
                    'timestamp': int(time.time()),
                }

                table.put_item(
                    Item=cached_account
                )

        return has_match


class AccountUtil:
    @staticmethod
    def get_accounts():
        return None


class MockAccountUtil:
    @staticmethod
    def get_accounts(user_id):
        table = CommonsUtil.get_dynamo_table(CommonsUtil.ACCOUNT_TABLE)

        if user_id is None:
            response = table.scan()
        else:
            response = table.query(
                KeyConditionExpression=Key('user_id').eq(user_id)
            )

        return response['Items']
