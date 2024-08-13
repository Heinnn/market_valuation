from dataset import Dataset
from utils.env import *
import pandas as pd
from retrying import retry

@retry(stop_max_attempt_number=10)
def interday_query(from_date, to_date, list_id):
    from_date = arrow.get(from_date)
    to_date = arrow.get(to_date)

    trading_date_universe_interday_df = dataset.db_collection.midman.query_div_adj_interdays(
        from_date=from_date,
        to_date=to_date,
        jitta_stock_ids=list_id
    )
    universe_price_df = trading_date_universe_interday_df.pivot(
        index='timestamp', values='close', columns='jitta_stock_id'
    )

    return universe_price_df

@retry(stop_max_attempt_number=7)
def query_data_from_sandbox(table, start, end, universe=None):
    df = pd.read_sql_query(f'''SELECT * FROM `{table}` ;''', con=cnx)
    df = df.pivot(index='seen', values='value', columns='jittaStockId')
    df = pd.DataFrame(df, index=pd.date_range(
        start=start, end=end, inclusive="both"))

    return df if universe is None else df[universe]
