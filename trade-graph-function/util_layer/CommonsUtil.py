from boto3.dynamodb.conditions import Key
import cbpro
from datetime import datetime, timedelta
import os
import boto3
import pytz
import json


LONDON_TMZ = pytz.timezone('Europe/London')


class CommonsUtil:
    ACCOUNT_TABLE = 'trader-account'
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
    def get_cbp_client():
        access_key = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-key')
        b64secret = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-secret')
        passphrase = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-passphrase')

        return cbpro.AuthenticatedClient(access_key, b64secret, passphrase)

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
        return LONDON_TMZ.localize(datetime.fromtimestamp(epoch_time / 1000)).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_transactions(account_id, days_back=14):
        table = CommonsUtil.get_dynamo_table(CommonsUtil.TRANSACTION_TABLE)
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
        accounts = AccountUtil.get_accounts(user_id)

        for account in accounts:
            if account['account_id'] == account_id:
                return True

        return False

    @staticmethod
    def error_message_response(error_message):
        return {
            "statusCode": 404,
            "headers": CommonsUtil.HEADERS,
            "body": json.dumps({
                "message": error_message
            }),
        }


class AccountUtil:
    @staticmethod
    def get_accounts(user_id):
        table = CommonsUtil.get_dynamo_table(CommonsUtil.ACCOUNT_TABLE)

        response = table.query(
            IndexName='user_id-index',
            KeyConditionExpression=Key('user_id').eq(user_id)
        )

        return response['Items']
