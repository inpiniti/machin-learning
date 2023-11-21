# pip i finnhub-python
import finnhub
api_key = "clblsshr01qp535sv26gclblsshr01qp535sv270"
finnhub_client = finnhub.Client(api_key=api_key)

# 국가 목록
# print(finnhub_client.country())

#    "code2": "US",
#    "code3": "USA",
#    "codeNo": "840",
#    "country": "United States",
#    "countryRiskPremium": 0,
#    "currency": "US Dollar",
#    "currencyCode": "USD",
#    "defaultSpread": 0,
#    "equityRiskPremium": 5,
#    "rating": "Aaa",
#    "region": "Americas",
#    "subRegion": "Northern America"

# 티커 목록
# print(finnhub_client.stock_symbols('US'))

#    "currency": "USD",
#    "description": "APPLE INC",
#    "displaySymbol": "AAPL",
#    "figi": "BBG000B9Y5X2",
#    "mic": "XNGS",
#    "symbol": "AAPL",
#    "type": "Common Stock"

us_stock_symbols = finnhub_client.stock_symbols('US')
print(us_stock_symbols.__len__())

# 'description'과 'symbol'만 추출
desc_and_symbol = [{'description': stock['description'], 'symbol': stock['symbol']} for stock in us_stock_symbols]
# print(desc_and_symbol)

print(finnhub_client.financials('AAPL', 'bs', 'annual'))