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

    # Delete the item passed
    table = CommonsUtil.get_dynamo_table(CommonsUtil.ACCOUNT_TABLE)
    table.delete_item(
        Key={
            'account_id': account_identifier
        })

    print(f'Managed account removed for {account_identifier} and user {user_id}')

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS
    }
