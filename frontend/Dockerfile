# frontent/Dockerfile

FROM python:3.9


ENV BACKEND_API="http://localhost:8000"

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit","run","app.py"]