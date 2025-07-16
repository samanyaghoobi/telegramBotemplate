FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# کاربر غیر روت
RUN useradd -m appuser
USER appuser

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["python", "run.py"]