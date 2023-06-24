import os

import whisper
from whisper.utils import format_timestamp
import yt_dlp
from yt_dlp.utils import download_range_func



model = whisper.load_model("small")


def process(file_name: str):
    # , decode_options= {'language' : 'ru'})
    result = model.transcribe(file_name, language="ru",
                              fp16=False)  # , verbose=True)
    text_file_name = file_name.split('/')[-1].split('.')[0]
    with open(f'./data/text/{text_file_name}.txt', 'w') as f:
        for i in range(len(result['segments'])):
            f.write('[' + f'{format_timestamp(result["segments"][i]["start"])}' + ' - ' +
                    f'{format_timestamp(result["segments"][i]["end"])}' + ']' + f'{result["segments"][i]["text"]}' + '\n')
    os.remove(file_name)

def download_audio_from_yotube(url: str, start_video=0, end_video=999999999) -> str:
    """
    Args:
    url - ссылка на видео
    start_video - начальный момент видео в секундах
    end_video - конечный момент видео в секундах
    """
    filename = 'video'
    ydl_opts_mp3 = {
        'format': 'bestaudio/best',
        'paths':
        {
            'home': './data/audio'
        },
        'download_ranges': download_range_func(None, [(start_video, end_video)]),
        'force_keyframes_at_cuts': True,
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    ydl_opts_mp4 = {
        'format': 'mp4',
        'paths':
        {
            'home': './data/video',
        },
            'download_ranges': download_range_func(None, [(start_video, end_video)]),
            'force_keyframes_at_cuts': True,
            'outtmpl': filename,
    }
    with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
        ydl.download([url])
    with yt_dlp.YoutubeDL(ydl_opts_mp4) as ydl:
        ydl.download([url])
    process(f'./data/audio/{filename}.mp3')  # Whisper
    with open(f'./data/text/{filename}.txt', 'r') as f:
        text = f.read()
    return text
