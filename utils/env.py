from yaml.loader import SafeLoader
import yaml
import numpy as np
# from dataset import Dataset
from sqlalchemy import create_engine
# import arrow


"""Manage env"""

REDIS_HOST = "192.168.142.7"
REDIS_PORT = 6379
REDIS_DB = 0
MYSQL_PASSWORD = "vbtrg564"
MYSQL_USER = "n2.boat"
MYSQL_STOCK_DB = "historical_dev"
MYSQL_BACKTEST_DB = "sandbox_backtest"
MYSQL_HOST = "192.168.142.5"
MYSQL_PORT = 3306
PROJECTK_HOST = "http://10.243.255.89:3000"
CACHE_TTL = 60 * 60 * 24 * 5
KONG_API_INTERDAY_MYSQL= "https://intel-api.dev.jitta.com/interdays"
KONG_API_KEY = 'Pwr42jPrCjFQfVEDj4e13huhGBkgP3OE'


# dataset = Dataset(
#     PROJECTK_HOST,
#     MYSQL_HOST,
#     MYSQL_PORT,
#     MYSQL_USER,
#     MYSQL_PASSWORD,
#     MYSQL_STOCK_DB,
#     MYSQL_BACKTEST_DB,
#     midman_host="http://192.168.142.44:3000",
# )

# load theme #TODO
with open("config/19themes.yaml") as f:
    data = yaml.load(f, Loader=SafeLoader)
themes = data["Themes"]
etf_universe_jids19 = list(map(lambda x: list(x.values())[0], themes))

with open("config/62themes.yaml") as f:
    data = yaml.load(f, Loader=SafeLoader)
themes = data["Themes"]
etf_universe_jids62 = list(map(lambda x: list(x.values())[0], themes))

# connect
host = "mysql+pymysql://{}:{}@{}:3306/{}".format(
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_BACKTEST_DB
)

cnx = create_engine(host)
# from_date = arrow.get(f"""{data["Date"]["start"]}T00:00:00.000Z""")
# to_date = arrow.get(f"""{data["Date"]["end"]}T00:00:00.000Z""")

HOLDING_PERIOD_LENGTH = data["HOLDING_PERIOD_LENGTH"]
HOLDING_PERIOD_TYPES = data["HOLDING_PERIOD_TYPES"]
HOLDING_PERIOD_TYPE = HOLDING_PERIOD_TYPES[1]

period_type_mapper = {
    "month": "M",
    "quarter": "Q",
    "year": "Y",
    "months": "M",
    "quarters": "Q",
    "years": "Y",
}
# ระยะเวลาถือหุ้น `1Q` = 1 Quarter, `2M` = 2 Months. etc.
HOLDING_PERIOD = f"{HOLDING_PERIOD_LENGTH}{period_type_mapper[HOLDING_PERIOD_TYPE]}"
NUM_REVENUE_GROWTH_RANK = data["NUM_REVENUE_GROWTH_RANK"]
NUM_HOLDING_ETF = data["NUM_HOLDING_ETF"]
PERIODS_IN_A_YEAR = 1

if period_type_mapper[HOLDING_PERIOD_TYPE] == "Y":
    PERIODS_IN_A_YEAR = 1 / HOLDING_PERIOD_LENGTH
    PERIOD_NUM_DAYS = 365
elif period_type_mapper[HOLDING_PERIOD_TYPE] == "M":
    PERIODS_IN_A_YEAR = 12 / HOLDING_PERIOD_LENGTH
    PERIOD_NUM_DAYS = int(np.floor(365 / PERIODS_IN_A_YEAR))
elif period_type_mapper[HOLDING_PERIOD_TYPE] == "Q":
    PERIODS_IN_A_YEAR = 4 / HOLDING_PERIOD_LENGTH
    PERIOD_NUM_DAYS = int(np.floor(365 / PERIODS_IN_A_YEAR))
