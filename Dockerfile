FROM python:3.12-slim

# 1) Create app folder
WORKDIR /app

# 2) Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy project source
COPY . .

# 4) Expose API port
EXPOSE 8000

# 5) Start FastAPI server
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]