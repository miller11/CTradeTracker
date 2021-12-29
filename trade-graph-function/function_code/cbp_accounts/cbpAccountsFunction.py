import cbpro
import simplejson as json
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event

    # todo Need to do some handling here. Look-up profile for user. String format the user access key
    access_key = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-key')
    b64secret = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-secret')
    passphrase = CommonsUtil.get_ssm_param('/ic-miller/trader-bot/ross/cb-access-passphrase')

    auth_client = cbpro.AuthenticatedClient(access_key, b64secret, passphrase)

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": auth_client.get_accounts()
        }),
    }
