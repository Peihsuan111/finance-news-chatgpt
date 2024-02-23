from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, dotenv_values
import math
import time
import tiktoken

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


def num_tokens_from_string(string: str, chosen_model: str) -> int:
    """Returns the number of tokens in a text string."""
    # encoding = tiktoken.get_encoding(encoding_name) # ex. encodeing_name = "cl100k_base"
    encoding = tiktoken.encoding_for_model(
        chosen_model
    )  # automatically load the correct encoding for a given model name
    num_tokens = len(encoding.encode(string))
    return num_tokens


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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
        documents = text_splitter.split_documents(loader.load())

        # Check documents token is over model limitation
        # Limitation of model text-embedding-ada-002 is 1,000,000 TPM
        total_tokens = num_tokens_from_string(str(documents), chosen_model)
        token_chunk_size = 800000  # buffer for limitation 1,000,000 TPM

        if total_tokens > 1000000:
            dividend_num = math.ceil(total_tokens / token_chunk_size)
            text_chunk_size = math.ceil(len(documents) / dividend_num)
            print(
                f"chunk documents to tokenize | chunk to {dividend_num} times; please wait at the {dividend_num} min."
            )

            init = True
            for i in range(0, len(documents), text_chunk_size):
                chunk = documents[i : i + text_chunk_size]
                print(f"processing documnets from to | {i}:{i + text_chunk_size}")
                if init:
                    vectorstore_chroma = Chroma.from_documents(
                        chunk, embeddings_opennai, persist_directory=db_path
                    )
                    time.sleep(60)
                    init = False
                else:
                    vectorstore_chroma.add_documents(chunk)
                    time.sleep(60)
        vectorstore_chroma.persist()
        print(
            f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')} | Load & Save vectorstore success!"
        )
    return vectorstore_chroma
