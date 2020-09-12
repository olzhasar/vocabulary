FROM python:3.8

RUN pip install pipenv

COPY Pipfile Pipfile.lock /
RUN pipenv install --system

COPY . /app
WORKDIR /app

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app", "--reload"]
