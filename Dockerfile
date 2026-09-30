FROM python:3.14-slim
LABEL authors="Duncan Maltman"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/app
COPY . .

CMD ["python", "main.py"]