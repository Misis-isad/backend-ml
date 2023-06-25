import time
import json
import httpx

from core.config import config


def ask(text: str) -> str:
    start = time.perf_counter()
    print("prompting gpt: ask")
    result = httpx.post(
        config["EDGE_GPT_HOST"] + "/ask", headers={
            'Content-Type': 'application/json'
        }, json={"text": text}, timeout=60000
    )
    print(time.perf_counter() - start)

    data = str(result.json())
    with open("last_data.txt", "w") as file:
        file.write(data)
    return data


def seo(text: str) -> str:
    print("prompting gpt: seo")
    start = time.perf_counter()
    result = httpx.post(
        config["EDGE_GPT_HOST"] + "/seo", headers={
            'Content-Type': 'application/json'
        }, json={"text": text}, timeout=60000
    )
    print(time.perf_counter() - start)
    data = str(result.json())
    # data = result.content.decode("utf-8")
    with open("last_data.txt", "w") as file:
        file.write(str(data))
    return data
