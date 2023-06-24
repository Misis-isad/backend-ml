import os
import cv2
import numpy as np

from typing import List, Tuple


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
                        cv2.imwrite(f'./data/{folder}/frame{start}.jpg', frame)
                        last_saved_frame = frame.copy()
                        timestamp = frame_count / fps
                        hours, remainder = divmod(timestamp, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        result[f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'] = f'./data/{folder}/frame{start}.jpg'
                        # timestamp_file.write(
                        #     f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}\n')
                        start += 1
                else:
                    cv2.imwrite(f'./data/{folder}/frame{start}.jpg', frame)
                    last_saved_frame = frame.copy()
                    timestamp = frame_count / fps
                    hours, remainder = divmod(timestamp, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    result[f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'] = f'./data/{folder}/frame{start}.jpg'
                    # timestamp_file.write(
                    # f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}\n')
                    start += 1
                count = 0
            prev_frame = frame.copy()
    os.remove(video_path)
    cap.release()

    return result


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


def insert_pic(text: str, file_t: str):
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

    # print(tcodes)
    return find_insertion_indices(times, tcodes)


if __name__ == "__main__":
    gav = '''Ваш текст'''
    insert_pic(gav, 'timestamps.txt')
