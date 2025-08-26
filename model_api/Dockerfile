FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

RUN mkdir -p /app/voice_messages

CMD ["uvicorn", "model_api:app", "--host", "0.0.0.0", "--port", "8086"]