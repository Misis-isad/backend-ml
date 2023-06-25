import os
import cv2
import numpy as np
import yt_dlp
import httpx

from typing import List, Tuple

BASE_URL = 'http://larek.itatmisis.ru:10000/static'


def upload_static(filename: str) -> str:
    url = BASE_URL + '/upload'
    upload_files = [
        ('file', (filename, open(filename, 'rb'), 'image/jpeg'))
    ]
    response = httpx.post(url, files=upload_files)
    return response.json()["link"]


def get_key_frames(freq: int, video_path: str) -> dict[str, str]:

    result = {}

    cap = cv2.VideoCapture(video_path)
    N = 60 * freq  # количество кадров для проверки
    folder = 'images'  # папка для сохранения изображений

    start = 1

    ret, prev_frame = cap.read()
    # if ret is None:
    #     ret, prev_frame = cap.read()
    prev_frame = cv2.resize(prev_frame, (640, 480))
    count = 0
    last_saved_frame = None
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0

    with open('timestamps.txt', 'w') as timestamp_file:
        while ret:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            frame = cv2.resize(frame, (640, 480))
            diff = cv2.absdiff(frame, prev_frame)
            if np.mean(diff) < 10:
                count += 1
            else:
                count = 0
            if count == N:
                if last_saved_frame is not None:
                    diff_last_saved = cv2.absdiff(frame, last_saved_frame)
                    if np.mean(diff_last_saved) > 10:
                        timestamp = frame_count / fps
                        hours, remainder = divmod(timestamp, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        cv2.imwrite(
                            f'./data/{folder}/{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.jpg', frame)
                        last_saved_frame = frame.copy()

                        filename = upload_static(
                            f'./data/{folder}/{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.jpg')
                        result[f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'] = filename
                        # result[f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'] = f'./data/{folder}/frame{start}.jpg'
                        timestamp_file.write(
                            f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}\n')
                        start += 1
                else:
                    timestamp = frame_count / fps
                    hours, remainder = divmod(timestamp, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    cv2.imwrite(
                        f'./data/{folder}/{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.jpg', frame)
                    last_saved_frame = frame.copy()
                    filename = upload_static(
                        f'./data/{folder}/{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.jpg')
                    result[f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'] = filename
                    # cv2.imwrite(f'./data/{folder}/frame{start}.jpg', frame)
                    # # httpx send file as form-data
                    # file = {'upload-file' : open(f'./data/{folder}/frame{start}.jpg', 'rb')}
                    # url = 'http://larek.itatmisis.ru:10000/static/upload'
                    # httpx.post(url, files=file)
                    # last_saved_frame = frame.copy()
                    # timestamp = frame_count / fps
                    # hours, remainder = divmod(timestamp, 3600)
                    # minutes, seconds = divmod(remainder, 60)
                    # result[f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'] = f'./data/{folder}/frame{start}.jpg'
                    timestamp_file.write(
                        f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}\n')
                    start += 1
                count = 0
            prev_frame = frame.copy()
    os.remove(video_path)
    cap.release()

    return result


def get_all_ids(images):
    res = httpx.get("http://larek.itatmisis.ru:10000/static/all")
    print(res)
    print(res.json())

    result = {}
    for filename in images.values():
        for el in res.json()["records"]:
            if el[1] == filename:
                result[filename] = f"{BASE_URL}/file/{el[0]}"

    return result


def generate_images(freq: int, video_path: str) -> dict[str, str]:
    images = get_key_frames(freq, video_path)
    return images


def find_insertion_indices(first: List[str], second: List[str]) -> List[Tuple[int, int]]:
    result = []
    for timecode in first:
        p = -1
        t = len(second)
        for i in range(len(second)):
            if second[i] < timecode:
                p = i
            else:
                t = i
                break
        result.append((p + 1, t + 1))
    return result


def insert_pictures(text: str, file_t: str):
    times = []
    with open(file_t, 'r') as f:
        for line in f:
            times.append(line.replace('\n', ''))
    print(times)

    tcodes = []
    i = 0
    while (i < len(text)):
        if text[i] == '[':
            i += 1
            buf = ''
            while text[i] != '.':
                buf += text[i]
                i += 1
            tcodes.append(buf)
        i += 1

    if len(tcodes[0]) == 5:
        tcodes = ['00:' + tcodes[i] for i in range(len(tcodes))]
    """"
    int_function
        return await dependant.call(**values)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/etarasov/Documents/backend-ml/main.py", line 104, in generate_article
        print(insert_pictures(result, "timestamps.txt"))
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/etarasov/Documents/backend-ml/core/tarakan.py", line 154, in insert_pictures
        if len(tcodes[0]) == 5:

    """
    # print(tcodes)
    return find_insertion_indices(times, tcodes)


def save_youtube_thumbnail(url: str):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        thumbnail_url = info_dict.get('thumbnail', None)
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            open('thumbnail.jpg', 'wb').write(response.content)


if __name__ == "__main__":
    gav = '''Ваш текст'''
    insert_pictures(gav, 'timestamps.txt')
