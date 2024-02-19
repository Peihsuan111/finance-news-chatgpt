# Importing all the required packages
from fastapi import FastAPI
import asyncio
from fastapi.responses import StreamingResponse
import uvicorn

# Generate wrapper function as discussed above
# Please extend this with the required functionality
# We are not returning anything as llm has already been tagged
# to the handler which streams the output
from rag_functiom import load_vectorstore
from langchain.chat_models import ChatOpenAI

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Importing Message templates
# from langchain.schema import HumanMessage
from handlers import MyCustomHandler
from threading import Thread
from queue import Queue
import os, yaml
from dotenv import dotenv_values
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import asyncio
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

# Creating a FastAPI app
app = FastAPI()

# Creating a Streamer queue
streamer_queue = Queue()

vectorstore = load_vectorstore()

# Creating an object of custom handler
my_handler = MyCustomHandler(streamer_queue)

llm = ChatOpenAI(
    temperature=0.0,
    model_name="gpt-3.5-turbo",
    streaming=True,
    callbacks=[my_handler],
)

prompt = """請用金融專家的角色，幫我根據以下新聞時事的文本回覆最底下的問題。若根據提供的文本，無法找到相關資訊請提供警示，不要嘗試生成內容。
這些文本將包含在三次回程中 (```)。

sentences :
```{context}```

question :{question}
請用繁體中文回覆
"""


PROMPT = PromptTemplate(template=prompt, input_variables=["context", "question"])

chain_type_kwargs = {"prompt": PROMPT, "verbose": True}


def generate(query):
    # llm.invoke([HumanMessage(content=query)])
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,  # chain_type='map_rerank',
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        # return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
    )

    print(
        f"{datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')} | Prepare Retrieval Chain!"
    )
    qa_chain(query)


def start_generation(query):
    # Creating a thread with generate function as a target
    thread = Thread(target=generate, kwargs={"query": query})
    # Starting the thread
    thread.start()


async def response_generator(query):
    # Start the generation process
    start_generation(query)

    # Starting an infinite loop
    while True:
        # Obtain the value from the streamer queue
        value = streamer_queue.get()
        # Check for the stop signal, which is None in our case
        if value == None:
            # If stop signal is found break the loop
            break

        yield value
        # Split the value into words
        # words = value.split()
        # for word in words:
        #     # Else yield the value
        #     yield word  # Send each word as a separate chunk

        # statement to signal the queue that task is done
        streamer_queue.task_done()

        # guard to make sure we are not extracting anything from
        # empty queue
        await asyncio.sleep(0.01)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/summary")
async def stream(query: str):
    print(f"Query receieved: {query}")
    return StreamingResponse(response_generator(query), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
