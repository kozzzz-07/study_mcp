FROM python:3.12-slim-bullseye

WORKDIR /app

COPY binance_mcp.py .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "binance_mcp.py"]
