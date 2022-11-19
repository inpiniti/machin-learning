import requests
import json

def naverApi(path):
    API_HOST = "https://api.stock.naver.com"
    url = API_HOST + path
    return sendApi(url)

def daumApi(path):
    API_HOST = "https://finance.daum.net"
    url = API_HOST + path
    sendApi(url, {
        "referer": "https://m.finance.daum.net/",
        "Accept": "*/*",
        "Host": "finance.daum.net",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    })

def sendApi(url, headers = {
    'Content-Type': 'application/json',
    'charset': 'UTF-8',
    'Accept': '*/*',
}):
    try:
        response = requests.get(url, headers=headers)

        list = []
        for i in response.json()["datas"]:
            list.append(i['stockName'])
        return list
    except Exception as ex:
        return ex

# 네이버 검색
def stock():
    return naverApi("/ranking/stock/local/total")

# 네이버 토론
def discussion():
    return naverApi("/ranking/discussion/local/stock_item")

# 네이버 뉴스
def news():
    return naverApi("/ranking/news/local/stock_local")

# 다음 인기
def popular():
    return daumApi("/content/debate/popular?type=STOCK&limit=10")

# 다음 조회 급등
def search():
    return daumApi("/api/search/ranks?limit=10")