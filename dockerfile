FROM python:3.9

RUN mkdir "/idempotent_methods"

WORKDIR "/idempotent_methods"

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--workers",  "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
