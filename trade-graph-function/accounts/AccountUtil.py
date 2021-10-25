import os
from coinbase.wallet.client import Client
import boto3


def get_cb_client():
    return Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))


def get_dynamo_table(table_name):
    if 'AWS_KEY_ID' in os.environ:
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_KEY_SECRET'))
    else:
        session = boto3.Session()

    dynamodb = session.resource('dynamodb', region_name='us-east-1')

    return dynamodb.Table(table_name)


class AccountUtil:
    @staticmethod
    def get_accounts():
        return get_cb_client().get_accounts(limit=50).data


class MockAccountUtil:
    @staticmethod
    def get_accounts():
        table = get_dynamo_table('cb-mock-account')
        response = table.scan()

        return response['Items']

