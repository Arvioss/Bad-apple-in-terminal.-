import os
import time
import sys
import urllib.request

VIDEO_URL = "https://media.githubusercontent.com/media/Arvioss/Lotm/main/videoplayback.mp4"
VIDEO_FILENAME = os.path.expanduser("~/.lotm_trailer.mp4")

ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]


def download_video():
    if os.path.exists(VIDEO_FILENAME):
        try:
            with open(VIDEO_FILENAME, "rb") as f:
                header = f.read(100)

            if b"git-lfs.github.com/spec" not in header:
                return

            os.remove(VIDEO_FILENAME)

        except Exception:
            pass

    try:
        print("Downloading video...")

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ("User-Agent", "Mozilla/5.0")
        ]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(VIDEO_URL, VIDEO_FILENAME)

        with open(VIDEO_FILENAME, "rb") as f:
            header = f.read(100)

        if b"git-lfs.github.com/spec" in header:
            print("Downloaded Git LFS pointer instead of video.")
            os.remove(VIDEO_FILENAME)
            sys.exit(1)

        print("Download complete.")

    except Exception as e:
        print("Download failed:", e)
        sys.exit(1)


def run_lotm():
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("Missing dependencies.")
        print("Install with:")
        print("pip install opencv-python numpy")
        sys.exit(1)

    download_video()

    cap = cv2.VideoCapture(VIDEO_FILENAME)

    if not cap.isOpened():
        print("Failed to open video.")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30

    frame_duration = 1 / fps

    try:
        columns, lines = os.get_terminal_size()
    except OSError:
        columns, lines = 80, 24

    width = min(columns - 2, 100)

    sys.stdout.write("\033[2J")
    sys.stdout.write("\033[H")
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

            target_height = max(
                1,
                int(width * aspect_ratio * 0.5)
            )

            resized = cv2.resize(
                gray,
                (width, target_height)
            )

            indices = (
                resized.astype(float)
                / 255
                * (len(ASCII_CHARS) - 1)
            ).astype(int)

            ascii_lines = [
                "".join(
                    ASCII_CHARS[i]
                    for i in row
                )
                for row in indices
            ]

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

        sys.stdout.write("\033[?25h")
        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[H")
        sys.stdout.flush()


if __name__ == "__main__":
    run_lotm()
