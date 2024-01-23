from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, dotenv_values
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import yaml
import os
import pandas as pd
import glob
import datetime

# load env token
with open("token.yaml", "r") as token_yaml:
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
        for f in glob.glob("./data/*.csv"):
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
            documents, embeddings_opennai, persist_directory="../chroma_db"
        )
        print(
            f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')} | Load & Save vectorstore success!"
        )
    return vectorstore_chroma


def retrieval_chain():
    vectorstore = load_vectorstore()

    llm = ChatOpenAI(temperature=0.0, model_name=chosen_model, streaming=True)
    prompt = """擔任金融分析師角色，請幫我根據以下新聞時事的文本回覆最底下的問題。若根據提供的文本，無法找到相關資訊請提供警示，不要嘗試生成內容。
    這些文本將包含在三次回程中 (```)。

    sentences :
    ```{context}```

    question :{question}
    請以專業金融分析師的角色用繁體中文回覆
    """

    PROMPT = PromptTemplate(template=prompt, input_variables=["context", "question"])

    chain_type_kwargs = {"prompt": PROMPT, "verbose": True}
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,  # chain_type='map_rerank',
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        # return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
    )

    print(
        f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')} | Prepare Retrieval Chain!"
    )
    return qa_chain


qa_chain = retrieval_chain()


def query_question(query):
    # query = "整理近兩週美國股市回顧及未來展望"
    # query = "亞洲股票市場的表現如何？亞洲股票市場包含「台灣、日本、中國、東南亞」等等的亞洲國家。幫我整理市場回顧及未來展望"
    response = qa_chain(query)
    return response
