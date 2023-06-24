import time
import json
import httpx

from core.config import config


def ask(text: str) -> dict:
    start = time.perf_counter()
    result = httpx.post(
        config["EDGE_GPT_HOST"] + "/ask", headers={
            'Content-Type': 'application/json'
        }, json={"text": text}, timeout=60000
    )
    print(time.perf_counter() - start)
    print(result.json())
    data = result.json()
    with open("last_data.txt", "w") as file:
        response_text = "".join([i["text"] for i in data])
        file.write(response_text)
    # with open("test.txt", "w") as file:
    #     for c in result.json():
    #         file.write(c)
    return result.json()
