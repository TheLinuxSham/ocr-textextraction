FROM python:3.13-slim-bookworm

RUN apt-get update \
    && apt-get install -y libgl1 tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY error_parsing.py .
COPY image_processing.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7654"]
