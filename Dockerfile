FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY platform ./platform
# OPENAI_API_KEY and REDIS_URL are injected at runtime.
CMD ["uvicorn", "platform.server:app", "--host", "0.0.0.0", "--port", "8000"]
