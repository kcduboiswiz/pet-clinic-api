FROM python:3.12-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./ 

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY ./src /app/src

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
