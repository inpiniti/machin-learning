# Python 3.8이 설치된 slim 버전의 Docker 이미지를 기반으로 새 Docker 이미지를 생성합니다.
FROM python:3.8-slim

# Docker 이미지 내에서 작업 디렉토리를 /app로 설정합니다.
WORKDIR /app

# 현재 디렉토리의 모든 파일과 디렉토리를 Docker 이미지의 /app 디렉토리에 복사합니다.
COPY . .

# 로컬에서 requirements.txt 파일의 모든 패키지를 wheel 파일로 빌드합니다:
# pip wheel -r requirements.txt -w ./wheels

# Copy the wheel files
#COPY ./wheels /wheels

# 패키지 목록을 최신 상태로 업데이트합니다.
RUN apt-get update
# 필요한 시스템 패키지를 설치합니다.
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install tk
#pip를 최신 버전으로 업그레이드합니다.
RUN pip3 install --upgrade pip
# 너무 오래 걸려서 아랫 부분 제거
RUN pip install --no-cache-dir -r requirements.txt

# Install the dependencies from the wheel files
#RUN pip install --no-cache-dir /wheels/*

# Docker 컨테이너가 5000번 포트를 사용하도록 설정
EXPOSE 5000

# Docker 컨테이너가 시작될 때 실행할 명령을 설정합니다. 
CMD ["python", "./app.py"]

