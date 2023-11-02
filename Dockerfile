FROM python:3.11-bullseye

WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--reload", "--port=8000", "--host=0.0.0.0"]