# frontent/Dockerfile

FROM python:3.9

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

ARG BACKEND_API
ENV BACKEND_API $BACKEND_API

COPY . /app
WORKDIR /app

EXPOSE 8501

CMD ["streamlit","run","app.py","False"]