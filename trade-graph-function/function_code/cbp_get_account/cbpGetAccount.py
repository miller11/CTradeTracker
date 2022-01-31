import cbpro
import simplejson as json
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event

    # Make sure user_id is passed and is authorized for the account
    try:
        user_id = event['requestContext']['authorizer']['claims']['cognito:username']
    except AttributeError:
        print("ERROR: user not authenticated ")
        return CommonsUtil.error_message_response("User not authenticated")

    # Check to make sure account-id is passed
    try:
        account_id = event['pathParameters']['id']  # Get account id from from query string
    except AttributeError:
        account_id = None

    if account_id is None:
        print("ERROR: no query string param passed " + event['pathParameters'])
        return CommonsUtil.error_message_response("No account_id query string param was passed")

    auth_client = CommonsUtil.get_cbp_client(user_id)

    account = auth_client.get_account(account_id)
    currency_price = auth_client.get_product_ticker(account['currency'] + '-USD')['price']

    account['usd_balance'] = float(account['balance']) * float(currency_price)
    account['current_price'] = currency_price

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": account
        }),
    }
