from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, dotenv_values

# from langchain.prompts import PromptTemplate
# from langchain.chains import RetrievalQA
# import asyncio
import yaml
import os
import pandas as pd
import glob
import datetime
from fastapi import FastAPI

# from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()


# load env token
from os import path

curpath = path.dirname(os.path.abspath(__file__))

with open(path.join(curpath, "token.yaml"), "r") as token_yaml:
    try:
        token = yaml.safe_load(token_yaml)
    except yaml.YAMLError as exc:
        print(exc)
api_key = token["openai_token"]
config = dotenv_values("../.env")
os.environ["OPENAI_API_KEY"] = api_key

db_path = "./chroma_db"
llm_model = ["gpt-3.5-turbo", "gpt-3.5-turbo-1106", "gpt-4-0314"]
chosen_model = llm_model[1]


def load_vectorstore():
    embeddings_opennai = OpenAIEmbeddings()
    if os.path.exists(db_path):
        # load existing db
        vectorstore_chroma = Chroma(
            persist_directory=db_path, embedding_function=embeddings_opennai
        )
        print(
            f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')} | Load vectorstore success!"
        )
    else:
        # read data and save db
        frames = []
        for f in glob.glob(path.join(curpath, "data/*.csv")):
            print(f"load file: {f}")
            data = pd.read_csv(f)
            data = data[["id", "title", "contents", "date", "category", "source"]]
            frames.append(data)
        df = pd.concat(frames)

        # load data
        loader = DataFrameLoader(df, page_content_column="contents")
        # split data
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        documents = text_splitter.split_documents(loader.load())
        # load & save db
        vectorstore_chroma = Chroma.from_documents(
            documents, embeddings_opennai, persist_directory=db_path
        )
        print(
            f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')} | Load & Save vectorstore success!"
        )
    return vectorstore_chroma
