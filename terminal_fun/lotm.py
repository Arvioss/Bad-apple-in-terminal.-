import os
import sys
import time
import gdown

VIDEO_ID = "170bTYQXHwmf289bGKG0PDo7c1EmViyWX"
VIDEO_FILENAME = os.path.expanduser("~/.lotm_trailer.mp4")

ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]


def download_video():
    if os.path.exists(VIDEO_FILENAME):
        if os.path.getsize(VIDEO_FILENAME) > 1024 * 1024:
            return
        os.remove(VIDEO_FILENAME)

    print("Downloading video...")

    try:
        gdown.download(
            id=VIDEO_ID,
            output=VIDEO_FILENAME,
            quiet=False,
            fuzzy=True
        )

        if not os.path.exists(VIDEO_FILENAME):
            print("Download failed.")
            sys.exit(1)

        print("Download complete.")

    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)


def run_lotm():
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("Missing dependencies.")
        print("Install with:")
        print("pip install gdown numpy opencv-python")
        sys.exit(1)

    download_video()

    cap = cv2.VideoCapture(VIDEO_FILENAME)

    if not cap.isOpened():
        print("Failed to open video.")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    frame_duration = 1.0 / fps

    try:
        columns, _ = os.get_terminal_size()
    except OSError:
        columns = 80

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

            ascii_frame = "\n".join(
                "".join(ASCII_CHARS[i] for i in row)
                for row in indices
            )

            sys.stdout.write("\033[H" + ascii_frame)
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
