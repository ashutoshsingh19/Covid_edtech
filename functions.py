import pandas as pd
from datetime import datetime
from datetime import timedelta

from statsmodels.tsa.seasonal import seasonal_decompose


def data_prep(df):
    df['time_stamp'] = df['timestamp'].dt.to_period('D')
    df = df.drop('timestamp', axis=1)
    df['tweet_counter'] = 1
    df = df.sort_values(by='time_stamp')
    df_col = df.groupby('time_stamp').sum()
    idx = pd.period_range(min(df_col.index), max(df_col.index))
    df_col = df_col.reindex(idx, fill_value=0)

    # uncomment this part to have a weekly basis of sampling

    df_col.index = df_col.index.to_timestamp()
    df_col = df_col.reset_index().rename(columns={'index': 'date_time'})
    df_col['week_time'] = df_col['date_time'].dt.to_period('W')
    df_col = df_col.groupby('week_time').sum()
    return df_col
