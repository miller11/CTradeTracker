from decimal import Decimal

import simplejson as json
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
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

    # Check to make sure that the body is passed
    try:
        new_account = json.loads(event['body'], parse_float=Decimal)['account']  # Get the body from the event
        new_account['account_id'] = account_identifier
        new_account['user_id'] = user_id
    except AttributeError:
        new_account = None

    if new_account is None:
        print("ERROR: no body with new account passed " + event['body'])
        return CommonsUtil.NO_ACCOUNT_RESPONSE

    # Save the new account
    table = CommonsUtil.get_dynamo_table(CommonsUtil.ACCOUNT_TABLE)
    table.put_item(
        Item=new_account
    )

    print(f'New account added for {account_identifier} and user {user_id}')

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS
    }
