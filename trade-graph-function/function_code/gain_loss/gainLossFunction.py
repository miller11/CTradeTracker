import json
import plotly.graph_objs as go
import pandas as pd

from TimeseriesUtil import TimeseriesUtil
from CommonsUtil import *


QUERY_STRING = """  SELECT time, measure_value::double as {}
                        FROM "account-tracker"."cbp-account" 
                        WHERE time between ago({}d) and now() 
                        AND account_id = '{}'
                        and measure_name = '{}'
                        ORDER BY time DESC """


def get_df(account_id, days_back):
    b_df = pd.DataFrame(TimeseriesUtil().run_query(QUERY_STRING.format('balance', days_back, account_id, 'balance')))
    g_df = pd.DataFrame(TimeseriesUtil().run_query(QUERY_STRING.format('gain', days_back, account_id, 'gain')))
    i_df = pd.DataFrame(TimeseriesUtil().run_query(QUERY_STRING.format('investment', days_back, account_id, 'investment')))

    t_df = pd.concat([b_df.set_index('time'), g_df.set_index('time'),  i_df.set_index('time')], axis=1, join='inner')

    t_df['balance'] = t_df['balance'].apply(lambda x: "${0:,.2f}".format(float(x)))
    t_df['gain'] = t_df['gain'].apply(lambda x: "${0:,.2f}".format(float(x)))
    t_df['investment'] = t_df['investment'].apply(lambda x: "${0:,.2f}".format(float(x)))

    return t_df


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

    # Check days back
    try:
        days_back = int(event['queryStringParameters']['days_back'])
    except AttributeError:
        days_back = 14

    df = get_df(account_identifier, days_back)
    fig = go.Figure()  # declare figure

    fig.add_trace(go.Scatter(x=df.index, y=df['balance'], line=dict(color='blue', width=1.5), name='balance'))
    fig.add_trace(go.Scatter(x=df.index, y=df['gain'], line=dict(color='green', width=1.5), name='gain'))
    fig.add_trace(go.Scatter(x=df.index, y=df['investment'], line=dict(color='orange', width=1.5), name='investment'))

    fig.update_yaxes(autorange="reversed")

    return {
        "statusCode": 200,
        "headers": CommonsUtil.HEADERS,
        "body": json.dumps({
            "message": fig.to_json()
        }),
    }
