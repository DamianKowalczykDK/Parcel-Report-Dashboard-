
FROM python:3.13-slim

ENV AUTHOR=Damian


ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip

RUN pip install pipenv && pipenv install --dev --system --deploy

COPY . .

ENV PORT=8501

CMD ["sh", "-c", "streamlit run main_2.py --server.port=$PORT --server.headless=true"]