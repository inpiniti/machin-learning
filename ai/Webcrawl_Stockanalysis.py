import requests #pip install requests
from bs4 import BeautifulSoup # pip install beautlfulsoup4
import pandas as pd # pip install pandas

tickers = ['aapl', 'tsla', 'nvda']
headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}

for ticker in tickers:
    # 연간: https://stockanalysis.com/stocks/aapl/financials/quarterly/
    url = "https://stockanalysis.com/stocks/{0}/financials/".format(ticker)
    
##    # 분기: https://stockanalysis.com/stocks/aapl/financials/quarterly/
##    url = "https://stockanalysis.com/stocks/{0}/financials/quarterly/".format(ticker)
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup)

    element_tables = soup.select("table[class='fintbl']")
    # element_tables = soup.select("div[class='overflow-x-auto']")
    # print(element_tables)

    
    df = pd.read_html(str(element_tables))[0] #'0번 테이블 뽑기
    print(df)

    #df.to_csv(ticker+'.csv', index=False, encoding='euc-kr')
    # 엑셀 파일로 저장하기용
    # df.to_excel(ticker+'.xlsx', index=False, encoding='euc-kr')


