import json
import httpx

from core.config import config


def ask(text: str) -> dict:
    result = httpx.post(
        config["EDGE_GPT_HOST"] + "/ask", headers={
            'Content-Type': 'application/json'
        }, data={"text": text}
    )
    return result.json()
