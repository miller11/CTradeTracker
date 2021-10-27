import json
from TimeseriesUtil import TimeseriesUtil
import plotly.graph_objs as go
import pandas as pd


QUERY_STRING = """  SELECT time, measure_value::double as {}
                        FROM "realized-gains"."ross-gains" 
                        WHERE time between ago(14d) and now() 
                        AND type = 'account'
                        and measure_name = '{}'
                        ORDER BY time DESC """


def get_df():
    b_df = pd.DataFrame(TimeseriesUtil().run_query(QUERY_STRING.format('balance', 'balance')))
    g_df = pd.DataFrame(TimeseriesUtil().run_query(QUERY_STRING.format('gain', 'gain')))
    i_df = pd.DataFrame(TimeseriesUtil().run_query(QUERY_STRING.format('investment', 'investment')))

    t_df = pd.concat([b_df.set_index('time'), g_df.set_index('time'),  i_df.set_index('time')], axis=1, join='inner')

    t_df['balance'] = t_df['balance'].apply(lambda x: "${0:,.2f}".format(float(x)))
    t_df['gain'] = t_df['gain'].apply(lambda x: "${0:,.2f}".format(float(x)))
    t_df['investment'] = t_df['investment'].apply(lambda x: "${0:,.2f}".format(float(x)))

    return t_df


def handler(event, context):
    print(json.dumps(event))  # Log the event
    print(event['requestContext']['accountId'])  # Log the account id

    # todo throw 403 if no user account

    if event['pathParameters']['account-id'] is None:
        print("ERROR: no query string param passed " + event['pathParameters'])

        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No account_id query string param was passed"
            }),
        }

    account_identifier = event['pathParameters']['account-id']  # Get account id from from query string

    df = get_df()
    fig = go.Figure()  # declare figure

    fig.add_trace(go.Scatter(x=df.index, y=df['balance'], line=dict(color='blue', width=1.5), name='balance'))
    fig.add_trace(go.Scatter(x=df.index, y=df['gain'], line=dict(color='green', width=1.5), name='gain'))
    fig.add_trace(go.Scatter(x=df.index, y=df['investment'], line=dict(color='orange', width=1.5), name='investment'))

    fig.update_yaxes(autorange="reversed")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,"
                                            "X-Requested-With,Accept,Access-Control-Allow-Methods,"
                                            "Access-Control-Allow-Origin,Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT",
            "X-Requested-With": "*",
            "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
        },
        "body": json.dumps({
            "message": fig.to_json()
        }),
    }
