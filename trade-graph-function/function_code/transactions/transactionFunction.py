import simplejson as json
from CommonsUtil import CommonsUtil


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

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": CommonsUtil.get_transactions(account_identifier)
        }),
    }
