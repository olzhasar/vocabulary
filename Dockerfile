FROM python:3.8

RUN pip install pipenv

COPY Pipfile Pipfile.lock /
RUN pipenv install --system

RUN pip install psycopg2

COPY . /app
WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "api.main:app", "--reload"]
