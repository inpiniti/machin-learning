FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glxFlask APP 을 배포하기 위한 도커파일
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install tk
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "./app.py"]
