import cv2, os, time, sys, shutil
import sounddevice as sd
import numpy as np

#Settings


ASCII_CHARS = r'''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''

COLORS = None
#Webcam
CAMERA_INDEX = 0

#Target FPS
FPS = 30

#Controlling terminal

def hide_cursor():
    print("\033[?25l", end="")

def show_cursor():
    print("\033[?25h", end ="")

def clear_screen():
    print("\033[2J\033[H")

def move_cursor_home():
    print("\033[H", end = "")

#Microphone input
def microphone_callback(indata, frames, time_info, status):
    if status:
        print(status)

    volume = np.linalg.norm(indata) * 10
    print(f"\rMicrophone volume: {volume:.2f}", end="")

#Frame to ASCII conversion

def frame_to_ascii(frame, width):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    height, original_width = gray.shape

    aspect_ratio = 0.5

    char_aspect = 0.5

    new_height = max(1, int(width * aspect_ratio * char_aspect))

    resized = cv2.resize(gray, (width, new_height), interpolation=cv2.INTER_AREA)
    resized_color = cv2.resize(color, (width, new_height), interpolation=cv2.INTER_AREA)
    resized_color = cv2.GaussianBlur(resized_color, (1, 1), 0)

    chars = ASCII_CHARS

    # Map grayscale pixels from 0-255 into the available character indexes.
    indexes = (resized.astype(int) * (len(chars) - 1)) // 255

    lines = []

    for row_index, row in enumerate(indexes):
        line = "".join(
            f"\033[38;2;{red};{green};{blue}m{chars[pixel]}"
            for pixel, (red, green, blue) in zip(row, resized_color[row_index])
        )
        lines.append(line)

    return "\n".join(lines) + "\033[0m"

#controlling the camera
def open_camera():
    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("ERROR COULD NOT OPEN CAMERA")
        print()
        print("Try changing camera from 0 to 1")
        sys.exit(1)

    return camera

#Microphone input
mic = sd.InputStream(
    device = 3,
    samplerate=44100,
    channels=1,
    callback=microphone_callback
)

mic.start()

def main():

    global WIDTH

    camera = open_camera()

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    clear_screen()
    hide_cursor()

    frame_time = 1/FPS

    try:

        while True:
            #returns time with most accuracy on clock tick
            start_time = time.perf_counter()

            success, frame = camera.read()

            if not success:
                move_cursor_home()
                print("Could not read webcam frame")
                continue



            # webcams are always mirrored and look weird so I'll flip it
            frame = cv2.flip(frame, 1)

            # convert the frame to ascii

            width = shutil.get_terminal_size().columns
            
            ascii_frame = frame_to_ascii(frame, width)

            # draw the frame

            move_cursor_home()

            sys.stdout.write(ascii_frame)
            sys.stdout.write("\033[J")
            sys.stdout.flush()

            # FPS limit

            elapsed = time.perf_counter() - start_time

            remaining = frame_time - elapsed
            if remaining > 0:
                time.sleep(remaining)

    except KeyboardInterrupt:
        pass

    finally:

        camera.release()
        mic.stop()
        mic.close()

        #restore terminal
        show_cursor()
        clear_screen()

        print("ASCII camera stopped")

if __name__ == "__main__":
    main()