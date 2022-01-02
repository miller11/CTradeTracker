import cbpro
import simplejson as json
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event

    # Check to make sure account-id is passed
    try:
        account_id = event['pathParameters']['id']  # Get account id from from query string
    except AttributeError:
        account_id = None

    if account_id is None:
        print("ERROR: no query string param passed " + event['pathParameters'])
        return CommonsUtil.error_message_response("No account_id query string param was passed")

    # todo Need to do some handling here. Look-up profile for user. String format the user access key
    access_key = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-key')
    b64secret = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-secret')
    passphrase = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-passphrase')

    auth_client = cbpro.AuthenticatedClient(access_key, b64secret, passphrase)

    account = auth_client.get_account(account_id)
    currency_price = auth_client.get_product_ticker(account['currency'] + '-USD')['price']

    account['usd_balance'] = float(account['balance']) * float(currency_price)

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": account
        }),
    }
