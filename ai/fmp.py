# pip install --upgrade certifi 
import pandas as pd
import numpy as np

api_key = 'rEJmKDBn9mAQHWvdg6PbBQU95gqLG7n8'
url_km='https://financialmodelingprep.com/api/v3/key-metrics/AAPL?period=annual&apikey='+api_key
pd_km = pd.read_json(url_km)

#url_is= "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=quarter&apikey={}".format(api_key)
#pd_is = pd.read_json(url_is)
#url_bs = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/AAPL?period=quarter&apikey={}".format(api_key)
#pd_bs = pd.read_json(url_bs)
#url_cf = "https://financialmodelingprep.com/api/v3/cash-flow-statement/AAPL?period=quarter&apikey={}".format(api_key)
#pd_cf = pd.read_json(url_cf)

#pd_mg = pd_is.merge(pd_bs,left_on=['date', 'symbol'], right_on=['date', 'symbol'], how='inner',suffixes=('', '_delme'))
#pd_mg = pd_mg.merge(pd_cf,left_on=['date', 'symbol'], right_on=['date', 'symbol'], how='inner',suffixes=('', '_delme'))

#pd_mg = pd_mg[[c for c in pd_mg.columns if not c.endswith('_delme')]]

print(pd_km)