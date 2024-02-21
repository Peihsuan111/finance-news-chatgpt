## Installation

Open a terminal and run:

```bash
$ pip install requirements.txt
```

## Quickstart
- Frontend 
  - Build Image
    ```bash
    $ cd frontend
    $ docker build --build-arg BACKEND_API="https://llm-backend-3nygwkh4ya-de.a.run.app" -t asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-frontend ./
    ```
- Backend
    ```bash
    $ cd backend
    $ docker build -t asia-east1-docker.pkg.dev/animated-spider-404200/ai-project/llm-backend ./
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