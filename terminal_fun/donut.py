import math
import time
import sys

def run_donut():
    a = 0
    b = 0
    
    # Hide cursor
    sys.stdout.write("\x1b[?25l")
    sys.stdout.flush()

    try:
        while True:
            z = [0] * 1760
            b_screen = [' '] * 1760
            
            j = 0
            while j < 6.28:
                j += 0.07
                i = 0
                while i < 6.28:
                    i += 0.02
                    
                    sin_i = math.sin(i)
                    cos_j = math.cos(j)
                    sin_a = math.sin(a)
                    sin_j = math.sin(j)
                    cos_a = math.cos(a)
                    cos_i = math.cos(i)
                    cos_b = math.cos(b)
                    sin_b = math.sin(b)
                    
                    h = cos_j + 2
                    d = 1 / (sin_i * h * sin_a + sin_j * cos_a + 5)
                    t = sin_i * h * cos_a - sin_j * sin_a
                    
                    x = int(40 + 30 * d * (cos_i * h * cos_b - t * sin_b))
                    y = int(12 + 15 * d * (cos_i * h * sin_b + t * cos_b))
                    o = int(x + 80 * y)
                    n = int(8 * ((sin_j * sin_a - sin_i * cos_j * cos_a) * cos_b - sin_i * cos_j * sin_a - sin_j * cos_a - cos_i * cos_j * sin_b))
                    
                    if 0 < y < 22 and 0 < x < 80 and d > z[o]:
                        z[o] = d
                        b_screen[o] = ".,-~:;=!*#$@"[n if n > 0 else 0]
            
            sys.stdout.write("\x1b[H")
            for k in range(1761):
                sys.stdout.write(b_screen[k] if k % 80 else '\n')
            sys.stdout.flush()
                
            a += 0.04
            b += 0.02
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        # Show cursor and clear screen
        sys.stdout.write("\x1b[?25h\x1b[2J\x1b[H")
        sys.stdout.flush()

if __name__ == "__main__":
    run_donut()
