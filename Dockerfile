FROM python:3.11-slim

WORKDIR /app

# Increase system limits for 50k threads
RUN ulimit -n 65535 && ulimit -u 65535

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "-u", "bot.py"]