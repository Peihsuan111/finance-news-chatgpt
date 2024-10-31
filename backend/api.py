from fastapi import FastAPI, Depends, Body, Header, HTTPException
from fastapi.responses import StreamingResponse
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import asyncio
import uvicorn
import os, yaml
from utils import load_vectorstore
from pydantic import BaseModel
from dependencies import get_token_header
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

# Using token.yaml openai api
with open("token.yaml", "r") as token_yaml:
    try:
        token = yaml.safe_load(token_yaml)
    except yaml.YAMLError as exc:
        print(exc)
os.environ["OPENAI_API_KEY"] = token["openai_token"]

# Load env token
config = dotenv_values("../.env")


chosen_model = "gpt-3.5-turbo"  # gpt-3.5-turbo-1106
app = FastAPI()


prompt = """請用金融專家的角色，幫我根據以下新聞時事的文本回覆最底下的問題。若根據提供的文本，無法找到相關資訊請提供警示，不要嘗試生成內容。
這些文本將包含在三次回程中 (```)。

sentences :
```{context}```

question :{question}
請用繁體中文回覆
"""

PROMPT = PromptTemplate(template=prompt, input_variables=["context", "question"])

vectorstore = load_vectorstore()
print(f"vectore store count: {vectorstore._collection.count()}")


llm = ChatOpenAI(
    temperature=0.0,
    model_name=chosen_model,
    streaming=True,
    callbacks=[],
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}, search_type="mmr"),
    # return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT, "verbose": True},
)


async def run_call(query: str, stream_it: AsyncIteratorCallbackHandler):

    # assign callback handler
    llm.callbacks = [stream_it]
    try:
        response = await qa_chain.acall(inputs={"query": query})
    except asyncio.TimeoutError:
        return {"error": "Response took too long"}
    return response


async def create_gen(query: str, stream_it: AsyncIteratorCallbackHandler):
    task = asyncio.create_task(run_call(query, stream_it))
    async for token in stream_it.aiter():
        yield token
    await task


# request input format
class Query(BaseModel):
    text: str


@app.get("/", dependencies=[Depends(get_token_header)])
async def root():
    return {"message": "Hello World"}


API_TOKENS = {"user1_token": "sk-123456789", "user2_token": "sk-987654321"}


@app.post("/chat", dependencies=[Depends(get_token_header)])
async def stream(query: Query = Body(...), authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split("Bearer ")[1]
    if token not in API_TOKENS.values():
        raise HTTPException(status_code=401, detail="Invalid Password Token!")
    else:
        stream_it = AsyncIteratorCallbackHandler()
        generator = create_gen(query.text, stream_it)
        return StreamingResponse(generator, media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
