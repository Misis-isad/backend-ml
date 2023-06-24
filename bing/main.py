from fastapi import FastAPI, UploadFile, File
import json
import logging
from ml import text_processing, create_prompt
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle


app = FastAPI()
bot: Chatbot | None = None

async def init():
    global bot
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
    try:
        bot = Chatbot.create(cookies=cookies) # type: ignore
    except Exception as e:
        logging.error(f"{e}")
        exit(-1)


async def shutdown():
    logging.info("shutting down")
    global bot
    await bot.close()


app.on_event("startup")(init)
app.on_event("shutdown")(shutdown)

@app.post("/ask")
async def ask_gpt(text: str):

    requests = create_prompt(text, "Prompt.txt")

    for index, request in enumerate(requests):
        print("sending request")
        response = await bot.ask(
                prompt=request,
                conversation_style=ConversationStyle.creative,
                simplify_response=True,
        )
        # save response to json file with name of chunk
        with open(f"chunk_{index}.json", "w") as file:
            json.dump(response, file, indent=2)
        print(json.dumps(response, indent=2))  # Returns
    """
    {
        "text": str
        "author": str
        "sources": list[dict]
        "sources_text": str
        "suggestions": list[str]
        "messages_left": int
    }
    """



