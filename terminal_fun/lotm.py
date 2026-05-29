import os
import sys
import time
import gdown
import cv2
import numpy as np

VIDEO_ID = "170bTYQXHwmf289bGKG0PDo7c1EmViyWX"
VIDEO_FILENAME = os.path.expanduser("~/.lotm_trailer.mp4")

ASCII_CHARS = " .:-=+*#%@"


def download_video():
    if os.path.exists(VIDEO_FILENAME):
        try:
            if os.path.getsize(VIDEO_FILENAME) > 10_000_000:
                return
            os.remove(VIDEO_FILENAME)
        except:
            pass

    print("Downloading video...")

    url = f"https://drive.google.com/uc?id={VIDEO_ID}"

    try:
        gdown.download(url, VIDEO_FILENAME, quiet=False)

        if not os.path.exists(VIDEO_FILENAME):
            raise RuntimeError("Video was not downloaded.")

        print("Download complete.")

    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)


def frame_to_ascii(frame, width):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    aspect_ratio = h / w

    height = max(1, int(width * aspect_ratio * 0.5))

    resized = cv2.resize(gray, (width, height))

    ascii_frame = []

    for row in resized:
        line = "".join(
            ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255]
            for pixel in row
        )
        ascii_frame.append(line)

    return "\n".join(ascii_frame)


def run_lotm():
    download_video()

    cap = cv2.VideoCapture(VIDEO_FILENAME)

    if not cap.isOpened():
        print("Failed to open video.")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    frame_delay = 1.0 / fps

    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 80

    width = min(terminal_width - 2, 100)

    print("\033[2J\033[H", end="")
    print("\033[?25l", end="")

    try:
        while True:
            start = time.time()

            ret, frame = cap.read()

            if not ret:
                break

            ascii_art = frame_to_ascii(frame, width)

            print("\033[H" + ascii_art, end="", flush=True)

            elapsed = time.time() - start

            if elapsed < frame_delay:
                time.sleep(frame_delay - elapsed)

    except KeyboardInterrupt:
        pass

    finally:
        cap.release()
        print("\033[?25h")
        print("\033[2J\033[H", end="")


if __name__ == "__main__":
    run_lotm()
