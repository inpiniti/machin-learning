# machin-learning

## 프로젝트 개요

`machin-learning` 프로젝트는 AI 및 데이터 분석 학습 목적으로 개발된 오픈소스 코드 베이스입니다.  
주요 기능은 다음과 같습니다.

- **금융 데이터 크롤링**: Naver, Daum, Investing, KRX(한국거래소), DART 등 다양한 금융 데이터 소스에서 데이터를 수집합니다.
- **데이터베이스 연동**: 수집된 데이터를 가공 및 저장하고, REST API로 제공합니다.
- **AI 예측/분석**: 수집된 데이터를 기반으로 다양한 AI/머신러닝 알고리즘을 활용한 예측 및 분석 기능을 제공합니다.
- **실시간 소켓 통신**: 웹소켓을 활용한 실시간 데이터 처리/전송 기능을 지원합니다.

## 전체 파일/폴더 트리 요약

```
machin-learning/
├── app.py               # Flask 웹 서버 및 API 엔드포인트 등록
├── requirements.txt     # 의존성 패키지 목록
├── ai/
│   └── yfinance_.py     # 야후파이낸스 등 AI 관련 데이터 핸들러
├── route/
│   ├── ai.py            # AI 예측 API
│   ├── daum.py          # Daum 증권 데이터 크롤링 API
│   ├── dart.py          # DART(전자공시) 데이터 수집 API
│   ├── db.py            # DB 조회 및 데이터 제공 API
│   ├── investing.py     # Investing.com 데이터 API
│   ├── krx.py           # KRX(한국거래소) 데이터 API
│   └── naver.py         # Naver 증권 데이터 API
├── utils/               # 데이터 처리 및 DB 유틸리티
├── socket_events.py     # 소켓 통신 이벤트 핸들러
├── templates/           # Flask 템플릿 폴더
├── static/              # 정적 파일(이미지, JS, CSS 등)
└── README.md
```

## API 엔드포인트 예시, 데이터 흐름, 실행 방법

### 실행 방법

```bash
# 의존 패키지 설치
pip install -r requirements.txt

# 서버 실행
python app.py
# 기본적으로 5001번 포트에서 실행됩니다.
```

### 주요 API 엔드포인트 예시

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET    | `/hello` | 헬로 테스트 |
| GET    | `/naver/crawling/Financial/<symbolCode>` | Naver 증권 재무 데이터 조회 |
| GET    | `/daum/crawling/Industries` | Daum 업종 데이터 크롤링 |
| GET    | `/daum/crawling/Stocks/<sector>` | Daum 업종별 종목 데이터 |
| GET    | `/daum/crawling/Financials` | Daum 전체 재무 데이터 일괄 크롤링 |
| GET    | `/krx/currentPrice` | KRX 현재 시세 데이터 |
| POST   | `/db/financials` | DB에서 조건별 재무 데이터 조회 (json body 필요) |
| GET    | `/dart/collect_data` | DART 데이터 일괄 수집 |
| GET    | `/ai/predict/<algorithm>/<market>/<analysis_period>` | AI 예측 결과 반환 |

> Swagger 문서: `/` (예: http://localhost:5001/)

### 데이터 흐름

1. **외부 데이터 수집**:  
   - `/naver`, `/daum`, `/krx`, `/investing`, `/dart` 등 엔드포인트에서 외부 금융 데이터를 크롤링합니다.
   - 크롤링된 데이터는 가공 후 DB에 저장되거나, 프론트엔드에 바로 제공합니다.

2. **DB 연동 및 가공**:  
   - `/db/financials` 등 엔드포인트에서 DB에 저장된 데이터를 조건에 따라 조회합니다.
   - 데이터 가공 후 JSON 형태로 반환합니다.

3. **AI 분석 및 예측**:  
   - `/ai/predict/...` 엔드포인트를 통해 저장된 모델 기반 예측 결과를 반환합니다.
   - 사용자는 알고리즘, 마켓, 분석 기간 등 파라미터를 조정해 다양한 예측 결과를 받을 수 있습니다.

4. **실시간 통신**:  
   - 소켓 통신(`flask_socketio`)을 활용하여 데이터 수집 상태, 진행률 등 실시간 정보를 전송합니다.

---

### 참고

- 배포 주소 (예시): http://20.214.141.2:5000
- Swagger 기반 API 문서 제공
- 각 엔드포인트 및 주요 파라미터, 응답 예시는 코드 내 Flask-Restx 주석 및 Swagger UI에서 확인 가능합니다.
