# frontent/Dockerfile

FROM python:3.9

ARG BACKEND_API

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]
CMD ["app.py", $BACKEND_API]