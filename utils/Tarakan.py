import cv2
import numpy as np

def Tarakan(freq: int, video_path: str):

    cap = cv2.VideoCapture(video_path)
    N = 60 * freq # количество кадров для проверки
    folder = 'images' # папка для сохранения изображений

    start = 1

    ret, prev_frame = cap.read()
    prev_frame = cv2.resize(prev_frame, (640, 480))
    count = 0
    last_saved_frame = None
    while ret:
        ret, frame = cap.read()
        if not ret:
            break
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
                    start += 1
            else:
                cv2.imwrite(f'./data/{folder}/frame{start}.jpg', frame)
                last_saved_frame = frame.copy()
                start += 1
            count = 0
        prev_frame = frame.copy()
    cap.release()

Tarakan(5, './data/video.mp4')