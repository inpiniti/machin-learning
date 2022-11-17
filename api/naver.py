import requests
import json

# 네이버 검색
def send_api(path, method):
    API_HOST = "http://www.example.com"
    url = API_HOST + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        "key1": "value1",
        "key2": "value2"
    }

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        print("response status %r" % response.status_code)
        print("response text %r" % response.text)
    except Exception as ex:
        print(ex)
ㅣ
# 네이버 토론
# 네이버 뉴스
# 다음 인기
# 다음 조회 급등


# 호출 예시
send_api("/test", "POST")