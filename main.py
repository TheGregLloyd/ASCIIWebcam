import cv2, os, time, sys, shutil

#Settings


ASCII_CHARS = r'''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''

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


#Frame to ASCII conversion

def frame_to_ascii(frame, width):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    height, original_width = gray.shape

    aspect_ratio = 0.5

    char_aspect = 0.5

    new_height = max(1, int(width * aspect_ratio * char_aspect))

    resized = cv2.resize(gray, (width, new_height), interpolation=cv2.INTER_AREA)

    chars = ASCII_CHARS

    # Map grayscale pixels from 0-255 into the available character indexes.
    indexes = (resized.astype(int) * (len(chars) - 1)) // 255

    lines = []

    for row in indexes:
        line = "".join(chars[pixel] for pixel in row)
        lines.append(line)

    return "\n".join(lines)

#controlling the camera
def open_camera():
    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("ERROR COULD NOT OPEN CAMERA")
        print()
        print("Try changing camera from 0 to 1")
        sys.exit(1)

    return camera

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

        #restore terminal
        show_cursor()
        clear_screen()

        print("ASCII camera stopped")

if __name__ == "__main__":
    main()