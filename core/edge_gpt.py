import httpx

from config import config


def ask(text: str) -> dict:
    result = httpx.post(
        config["EDGE_GPT_HOST"] + "/ask", data={
            "text": text
        }
    )
    return result.json()
