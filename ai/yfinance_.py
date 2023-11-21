# yahoo-finance reader
#pip install yfinance
import yfinance as yf

import pandas as pd

import finnhub
api_key = "clblsshr01qp535sv26gclblsshr01qp535sv270"
finnhub_client = finnhub.Client(api_key=api_key)

## apple 재무정보 물러오기 
#aapl_yf =yf.Ticker('AAPL')
#aapl_yf =yf.Ticker('005930.KS')


#aapl_data =  aapl_yf.financials # 재무정보 
#print(aapl_data)

print('=====================================================')

# 특정 분기의 데이터를 얻으려면, period 매개변수를 'quarter'로 설정
#print(aapl_yf.quarterly_financials)

# Tax Effect Of Unusual Items
# Tax Rate For Calcs
# Normalized EBITDA
# Net Income From Continuing Operation Net Minori...
# Reconciled Depreciation
# Reconciled Cost Of Revenue
# EBITDA
# ...
# Net Income
# Pretax Income
# Operating Income

code = ['AD', 'AQ', 'AS', 'AT', 'AX', 'BA', 'BC', 'BD', 'BE', 'BH', 'BK', 'BO', 'BR', 'CA', 'CN', 'CO', 'CR', 'CS', 'DB', 'DE', 'DS', 'DU', 'F', 'HE', 'HK', 'HM', 'IC', 'IR', 'IS', 'JK', 'JO', 'KL', 'KQ', 'KS', 'KW', 'L', 'LN', 'LS', 'MC', 'ME', 'MI', 'MU', 'MX', 'NE', 'NL', 'NS', 'NZ', 'OL', 'PA', 'PM', 'PR', 'QA', 'RG', 'SA', 'SG', 'SI', 'SN', 'SR', 'SS', 'ST', 'SW', 'SZ', 'T', 'TA', 'TL', 'TO', 'TW', 'TWO', 'TU', 'US', 'V', 'VI', 'VN', 'VS', 'WA', 'XA', 'HA', 'SX', 'TG', 'SC', 'SL']

def print_financials():
    us_stock_symbols = finnhub_client.stock_symbols('V')

    # us_stock_symbols 루프문 돌면서 symbol 출력
    for stock in us_stock_symbols:
        print(stock['description'])

        sb = stock['symbol']
        tk =yf.Ticker(sb)

        # ticker 로 재무정보 물러오기
        fnc = tk.quarterly_financials

        # 행과 열 변경
        #fnc = fnc.transpose()

        try:
            # 'Net Income', 'Pretax Income', 'Operating Income' 열만 선택
            npo_fnc = fnc.loc[['Net Income', 'Pretax Income', 'Operating Income']]

            # 재무재표 출력
            print(npo_fnc)
        except:
            print('Error')

print_financials()