import os
from fastapi import FastAPI, APIRouter, BackgroundTasks

from core.schemas import RecordDto, RecordSettings
from core.whisper import download_audio_from_yotube
from core.edge_gpt import ask
from core.tarakan import get_key_frames

app = FastAPI()

# add fucntion which will send request to edge_gpt as a background task


async def send_request_to_edge_gpt(text: str):
    data = ask(text)


def on_startup():
    # check if data folder exists
    if not os.path.exists('./data'):
        os.mkdir('./data')
    # check if data/video folder exists
    if not os.path.exists('./data/video'):
        os.mkdir('./data/video')
    # check if data/audio folder exists
    if not os.path.exists('./data/audio'):
        os.mkdir('./data/audio')
    # check if data/text folder exists
    if not os.path.exists('./data/text'):
        os.mkdir('./data/text')
    # check if data/images folder exists
    if not os.path.exists('./data/images'):
        os.mkdir('./data/images')


@app.post("/generate_article")
async def generate_article(record_data: RecordDto):

    if record_data.start_timecode == "":
        record_data.start_timecode = "00:00:00"
    if record_data.end_timecode == "":
        record_data.end_timecode = "99:99:99"

    start_seconds = sum(
        [60 * int(t) * (3-i) for i, t in enumerate(record_data.start_timecode.split(':'))])
    end_seconds = sum(
        [60 * int(t) * (3-i) for i, t in enumerate(record_data.end_timecode.split(':'))])

    whisper_text = download_audio_from_yotube(
        record_data.video_link, start_seconds, end_seconds)

    # send request to edge_gpt
    # result = ask(whisper_text)
    # results cames as list of dicts with keys:
    # {
    #     "text": str
    #     "author": str
    #     "sources": list[dict]
    #     "sources_text": str
    #     "suggestions": list[str]
    #     "messages_left": int
    # }
    # we need to combine all texts into one string and return it as html
    # html = " ".join([r for r in result])

    print(get_key_frames(5, "data/video/video"))

    # html, title для рекорда и ссылку на превью
    return {
        "html": "ok",
        "title": "title",
    }

    # dowload video
    # whisper
    # tarakan
    #  return {}...
    ...
