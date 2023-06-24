import os
from fastapi import FastAPI, APIRouter, BackgroundTasks

from utils.schemas import RecordDto, RecordSettings
from utils.whisper import download_audio_from_yotube

app = FastAPI()


def on_startup():
    # check if data folder exists
    if not os.path.exists('./data'):
        os.mkdir('./data')
        os.mkdir('./data/audio')
        os.mkdir('./data/video')
        os.mkdir('./data/text')
    if not all(os.path.exists(path) for path in ['./data/audio', './data/video', './data/text']):
        os.mkdir('./data/audio')
        os.mkdir('./data/video')
        os.mkdir('./data/text')


@app.post("/generate_article")
async def generate_article(record_data: RecordDto):
    if record_data.settings.start_timecode == "":
        record_data.settings.start_timecode = "00:00:00"
    if record_data.settings.end_timecode == "":
        record_data.settings.end_timecode = "99:99:99"

    start_seconds = sum(
        [60 * int(t) * (3-i) for i, t in enumerate(record_data.settings.start_timecode.split(':'))])
    end_seconds = sum(
        [60 * int(t) * (3-i) for i, t in enumerate(record_data.settings.end_timecode.split(':'))])

    audio = download_audio_from_yotube(
        record_data.video_link, start_seconds, end_seconds)

    # create background task

    return {
        "id": 1,
        "status": "processing"
    }

    # dowload video
    # whisper
    # tarakan
    #  return {}...
    ...
