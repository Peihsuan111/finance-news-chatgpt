# frontent/Dockerfile

FROM python:3.9

ARG BACKEND_API

ENV BACKEND_API $BACKEND_API

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit","run","app.py"]