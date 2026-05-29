import os
import time
import sys
import urllib.request

# Global configuration
VIDEO_URL = "https://github.com/bad-apple-lab/Bad-Apple/raw/main/badapple.mp4"
VIDEO_FILENAME = os.path.expanduser("~/.bad_apple.mp4")
ASCII_CHARS = ["1","0"]

def download_video():
    if not os.path.exists(VIDEO_FILENAME):
        print(f"Downloading Bad Apple video (~5MB) to {VIDEO_FILENAME}...")
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(VIDEO_URL, VIDEO_FILENAME)
            print("Download complete.\n")
        except Exception as e:
            print(f"Error downloading video: {e}")
            print("You might need to download it manually and place it at ~/.bad_apple.mp4")
            sys.exit(1)

def run_bad_apple():
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("Error: 'opencv-python' and 'numpy' are required for this command.")
        print("Please install them with: pip install opencv-python numpy")
        sys.exit(1)

    download_video()
    
    cap = cv2.VideoCapture(VIDEO_FILENAME)
    if not cap.isOpened():
        print(f"Error: Could not open video file at {VIDEO_FILENAME}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: fps = 30
    frame_duration = 1 / fps

    # Get terminal size
    try:
        columns, lines = os.get_terminal_size()
    except OSError:
        columns, lines = 80, 24

    # Target width (leave some room)
    width = min(columns - 2, 100)

    # Hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            start_time = time.time()
            
            # Grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Resize
            h, w = gray.shape
            aspect_ratio = h / w
            target_height = int(width * aspect_ratio * 0.5) # 0.5 for terminal char aspect ratio
            resized = cv2.resize(gray, (width, target_height))
            
            # Map to ASCII
            # Optimization: use numpy to map pixels to indices
            indices = (resized.astype(float) / 255 * (len(ASCII_CHARS) - 1)).astype(int)
            ascii_lines = []
            for row in indices:
                line = "".join([ASCII_CHARS[i] for i in row])
                ascii_lines.append(line)
            
            # Render
            output = "\033[H" + "\n".join(ascii_lines)
            sys.stdout.write(output)
            sys.stdout.flush()
            
            # Sync
            elapsed = time.time() - start_time
            if elapsed < frame_duration:
                time.sleep(frame_duration - elapsed)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\033[?25h\033[2J\033[H")
        sys.stdout.flush()
        print("Playback finished.")

if __name__ == "__main__":
    run_bad_apple()
