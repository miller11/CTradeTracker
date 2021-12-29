import json
from CommonsUtil import CommonsUtil


def lambda_handler(event, context):
    print(json.dumps(event))  # Log the event
