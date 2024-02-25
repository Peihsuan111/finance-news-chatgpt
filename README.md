## Installation

Open a terminal and run:

```bash
$ cd backend
$ pip install requirements.txt

$ cd frontend
$ pip install requirements.txt
```

## Quickstart
```
Make sure you put token.yaml inside ./frontend & ./backend folder

token.yaml
`
header_token: RANDOM_HEADER_TOKEN
`
``` 

### Run locally
- Backend
  ```
  $ cd backend
  $ python3 api.py
  ```
- Frontend
  ```
  $ cd frontend
  $ streamlit run app.py True
  ```

### Deploy on GCP
- Setup beforehand: 
  1. Create a GCP Project
  2. Open Artifact Registry repository(ex. `ai-project`). Also, make sure repository has right permission >> `Artifact Registry存放區管理員`

- argv: (change these argv to your own)
  - gcp project name: `animated-spider-404200`
  - artifact registry: `ai-project`

- Backend
    ```bash
    $ cd backend
    $ docker build -t asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-backend ./

    $ docker push asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-backend
    ```

- Frontend 
  - Build Image
  ```bash
  $ cd frontend
  $ docker build --build-arg BACKEND_API="https://llm-backend-3nygwkh4ya-de.a.run.app" -t asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-frontend ./

  $ docker push asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-frontend
  ```
    
- embedding module
    ```
    transformers==4.31.0
    sentence-transformers==2.2.2
    accelerate==0.21.0
    einops==0.6.1
    xformers==0.0.20
    bitsandbytes==0.41.0
    ```