# pip install inpinitiFinance
import ifinance

api_key = '9264c9a7d0da3f3ab83b509033a337722b5c329f'

ifinance.set_api_key(api_key)

dart = ifinance.get_financial_dataframe('005930')
print(dart)
print('-' * 80)

krx = ifinance.get_monthly_stock_dataframe('KR7005930003')
print(krx)
print('-' * 80)

dart_krx = ifinance.merge_financial_and_monthly_stock_dataframe(dart, krx)
print(dart_krx)
print('-' * 80)