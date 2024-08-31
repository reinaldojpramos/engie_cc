FROM python:3.9-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8888

ENV FLASK_ENV=development

CMD ["poetry", "run", "python", "app.py"]
