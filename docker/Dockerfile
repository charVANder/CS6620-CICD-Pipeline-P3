FROM python:3.10
WORKDIR /app
COPY requirements.txt .
# adding no-cache-dir b/c I read it was better for CI/CD pipelines
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY app.py .

# Run API server (until manually stopped)
CMD ["python", "app.py"]