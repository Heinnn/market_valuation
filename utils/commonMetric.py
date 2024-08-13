import pandas as pd
from dateutil.relativedelta import relativedelta


def period_return(nav: pd.DataFrame(), start, end):
    # assert pd.to_datetime(start) >= nav.index[0], 'out of datarange'
    # assert pd.to_datetime(end) <= nav.index[-1], 'out of datarange'

    return (nav.loc[end] - nav.loc[start]) / nav.loc[start]


def cagr(nav : pd.DataFrame(), start, end):
    """Calculate the CAGR for a given time period."""
    st = pd.to_datetime(start)
    en = pd.to_datetime(end)
    difference = relativedelta(en, st)
    difference_in_years = difference.years + \
        difference.months/12 + difference.days/365.2425
    totalreturn = (nav.loc[end] - nav.loc[start]) / nav.loc[start]
    cagr = (1+totalreturn)**(1/difference_in_years) - 1

    return cagr
