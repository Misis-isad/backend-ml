import os
from fastapi import FastAPI, APIRouter, BackgroundTasks

from core.text import to_html
from core.schemas import RecordDto, RecordSettings
from core.whisper1 import download_audio_from_yotube
from core.edge_gpt import ask, seo
from core.tarakan import generate_images, insert_pictures

app = FastAPI()

# add fucntion which will send request to edge_gpt as a background task
PROCESSING_STAUS = {

}


def send_request_to_edge_gpt(whisper_text: str, images: dict = {}, video_url: str = ""):
    global PROCESSING_STAUS
    if video_url:
        PROCESSING_STAUS[video_url] = "prompt1"
        result = ask(whisper_text)
        PROCESSING_STAUS[video_url] = "prompt2"
        result = seo(result)
        PROCESSING_STAUS[video_url] = "parcing"
        result = to_html(result)
        PROCESSING_STAUS.pop(video_url)
        print(result)
    else:
        result = ask(whisper_text)
        result = seo(result)
        result = to_html(result)


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


@app.post("/test")
async def test(
    record_data: RecordDto,
    background_tasks: BackgroundTasks
):

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
    images = generate_images(5, "data/video/video")
    background_tasks.add_task(send_request_to_edge_gpt, whisper_text)
    return {
        "status": "started processing",
        "images": images
    }
    print("result afrer seo")
    print(result)
    print("-"*40)

    print(images)

    print(insert_pictures(result, "timestamps.txt"))

    return {
        "body": result,
        "title": "title",
        "images": images
    }


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

    result = ask(whisper_text)
    result = seo(result)
    result = to_html(result)
    print("result afrer seo")
    print(result)
    print("-"*40)
    images = generate_images(5, "data/video/video")
    print(images)

    # print(insert_pictures(result, "timestamps.txt"))

    return {
        "body": result,
        "title": "title",
        "images": images
    }
