from typing import Annotated
from fastapi import Header, HTTPException
import yaml

# get header x-token
with open("token.yaml", "r") as token_yaml:
    try:
        token = yaml.safe_load(token_yaml)
    except yaml.YAMLError as exc:
        print(exc)

header_token = token["header_token"]


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != header_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
