## Installation

Open a terminal and run:

```bash
$ pip install requirements.txt
```

## Quickstart
- Frontend
    ```bash
    $ streamlit run 1_News_Summarizer.py
    ```
- Backend
    ```bash
    $ python3 api.py
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