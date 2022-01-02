import simplejson as json
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event

    # todo Need to do some handling here. Look-up profile for user. String format the user access key
    auth_client = CommonsUtil.get_cbp_client()

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "data": auth_client.get_accounts()
        }),
    }
