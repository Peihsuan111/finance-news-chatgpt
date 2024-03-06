<!-- 專案簡介 -->
## About The Project

* LLM + RAG Inplement
  * RAG Dataset(新聞時間區間: 2023年10,11月):
    * [鉅亨網](https://www.cnyes.com)
    * [MoneyDj理財網](https://www.moneydj.com)
    * [經濟日報](https://money.udn.com/money/index)
    * [聯合報](https://udn.com/news/index)
    * [Yahoo新聞](https://tw.stock.yahoo.com/rss-index/)
* Let LLM answer your question based on your own dataset.

## Installation

Open a terminal and run:

```bash
cd backend
pip install requirements.txt

cd frontend
pip install requirements.txt
```

## How to use?

*1.* Make sure you put token.yaml inside ./frontend & ./backend folder

* token.yaml:

     ```
     openai_token: YOUR_OPENAI_TOKEN
     header_token: RANDOM_HEADER_TOKEN
     sara_token: RANDOM_ACCESS_TOKEN
     ```

     [Get OPENAI API TOKEN](https://platform.openai.com/docs/quickstart?context=python)

### (Option 1)Run locally

* Backend

  ```
  cd backend
  python3 api.py
  ```

* Frontend

  ```
  cd frontend
  streamlit run app.py True
  ```

### (Option 2)Deploy on GCP

1. GCP Setup:
   1. Create a GCP Project
   2. Open Artifact Registry repository(ex. `ai-project`). Also, make sure repository has right permission >> `Artifact Registry存放區管理員`

2. Change these argv to your own
     * gcp project name: `animated-spider-404200`
     * artifact registry: `ai-project`

3. Build docker image

* Backend

    ```bash
    cd backend
    docker build -t asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-backend ./

    docker push asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-backend
    ```

* Frontend
  * Build Image

  ```bash
  cd frontend
  docker build --build-arg BACKEND_API="https://llm-backend-3nygwkh4ya-de.a.run.app" -t asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-frontend ./

  docker push asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-frontend
  ```

## Other module usage

* embedding module

    ```
    transformers==4.31.0
    sentence-transformers==2.2.2
    accelerate==0.21.0
    einops==0.6.1
    xformers==0.0.20
    bitsandbytes==0.41.0
    ```

<!-- DEMO -->
## DEMO

- Front Page
![front-end page1](/img/frontend-page.png?raw=true "Demo Page 1")

* Demo
![front-end page2](/img/frontend-page-demo.png?raw=true "Demo Page 2")
