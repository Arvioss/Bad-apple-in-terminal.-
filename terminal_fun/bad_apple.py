import os
import time
import sys
import urllib.request

VIDEO_URL = "https://github.com/bad-apple-lab/Bad-Apple/raw/main/badapple.mp4"
AUDIO_URL = "https://raw.githubusercontent.com/CalvinLoke/bad-apple/master/bad-apple-audio.mp3"
VIDEO_FILENAME = os.path.expanduser("~/.bad_apple.mp4")
AUDIO_FILENAME = os.path.expanduser("~/.bad_apple.mp3")
ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

def download_assets():
    for url, filename in [(VIDEO_URL, VIDEO_FILENAME), (AUDIO_URL, AUDIO_FILENAME)]:
        if not os.path.exists(filename):
            try:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, filename)
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                sys.exit(1)

def run_bad_apple():
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("Please install opencv-python and numpy.")
        sys.exit(1)

    # Try to import audio dependencies
    has_audio = False
    try:
        import pygame
        pygame.mixer.init()
        has_audio = True
    except ImportError:
        print("Note: Install 'pygame' for audio support.")
    except Exception as e:
        print(f"Note: Audio initialization failed: {e}")

    download_assets()
    
    cap = cv2.VideoCapture(VIDEO_FILENAME)
    if not cap.isOpened():
        print(f"Error: Could not open video file {VIDEO_FILENAME}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: fps = 30
    frame_duration = 1 / fps

    try:
        columns, lines = os.get_terminal_size()
    except OSError:
        columns, lines = 80, 24

    width = min(columns - 2, 100)

    # Initialize audio
    if has_audio:
        try:
            pygame.mixer.music.load(AUDIO_FILENAME)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing audio: {e}")
            has_audio = False

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
        if has_audio:
            pygame.mixer.music.stop()
        cap.release()
        sys.stdout.write("\033[?25h\033[2J\033[H")
        sys.stdout.flush()

if __name__ == "__main__":
    run_bad_apple()
