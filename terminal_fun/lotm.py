import os
import time
import sys
import urllib.request

VIDEO_URL = "https://github.com/Arvioss/Lotm/raw/main/videoplayback.mp4"
VIDEO_FILENAME = os.path.expanduser("~/.lotm_trailer.mp4")
ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

def download_video():
    if not os.path.exists(VIDEO_FILENAME):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(VIDEO_URL, VIDEO_FILENAME)
        except Exception:
            sys.exit(1)

def run_lotm():
    try:
        import cv2
        import numpy as np
    except ImportError:
        sys.exit(1)

    download_video()
    
    cap = cv2.VideoCapture(VIDEO_FILENAME)
    if not cap.isOpened():
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: fps = 30
    frame_duration = 1 / fps

    try:
        columns, lines = os.get_terminal_size()
    except OSError:
        columns, lines = 80, 24

    width = min(columns - 2, 100)

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            start_time = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            h, w = gray.shape
            aspect_ratio = h / w
            target_height = int(width * aspect_ratio * 0.5)
            resized = cv2.resize(gray, (width, target_height))
            
            indices = (resized.astype(float) / 255 * (len(ASCII_CHARS) - 1)).astype(int)
            ascii_lines = ["".join([ASCII_CHARS[i] for i in row]) for row in indices]
            
            output = "\033[H" + "\n".join(ascii_lines)
            sys.stdout.write(output)
            sys.stdout.flush()
            
            elapsed = time.time() - start_time
            if elapsed < frame_duration:
                time.sleep(frame_duration - elapsed)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\033[?25h\033[2J\033[H")
        sys.stdout.flush()

if __name__ == "__main__":
    run_lotm()
