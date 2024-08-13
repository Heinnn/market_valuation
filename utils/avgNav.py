'''aggregate all prices in df to avg nav'''


def prices_to_avg_nav(price_df, start, end=None):
    price_diff = price_df.pct_change()

    if end:
        price_range = price_df.loc[(price_df.index >= start) &
                                   (price_df.index <= end)]
    else:
        price_range = price_df.loc[(price_df.index >= start)]

    pct_change = price_range.pct_change()
    mean = pct_change.mean(axis=1)
    initial_price = 10  # Starting price
    nav = (1 + mean).cumprod() * initial_price
    ffill = nav.resample('d').ffill()

    return ffill
