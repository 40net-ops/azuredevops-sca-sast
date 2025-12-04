FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PYTHONPATH=/app
ENV FLASK_APP=app/main.py
CMD ["python", "app/main.py"]

