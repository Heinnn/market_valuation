import pandas as pd
import numpy as np


def to_rank_df(rank:'json', end): # pd.read_json then parse to argument "rank"
    
    # manage rank
    date = []
    list_rank = []
    for i in range(len(rank)):
        date.append(rank.iloc[i].date.strftime('%Y-%m-%d'))
        list_rank.append([d['jittaStockId'] for d in rank.iloc[i]['ranking']])
        
    rank_df = pd.DataFrame({'date':date,
              'rank':list_rank})
    rank_df = rank_df.append({'date':end,'rank':list_rank[-1]},ignore_index=True)
    rank_df['date'] = pd.to_datetime(rank_df['date'])
    rank_df.set_index('date', inplace=True)
    resample_rank_df = rank_df.resample('d').ffill()
    
    return resample_rank_df


def selected_price_df(price_df, rankdf):
    df = price_df.loc[price_df.index >= rankdf.index[0]]
    for i in df.index:
        i = i.strftime('%Y-%m-%d')
        to_nan = list(set(df.columns) - set(list(rankdf.loc[i])[0][:4])) # force non-rank Id to nan
        df.loc[i][to_nan]=np.nan

    return df