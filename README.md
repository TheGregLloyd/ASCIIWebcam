# ASCII Webcam

A small Python program that captures live video from your webcam and displays it as ASCII art in the terminal.

## Requirements

- Python 3.8 or newer
- A working webcam
- A terminal that supports ANSI escape codes, such as Windows Terminal or the VS Code integrated terminal

## Setup

1. Open a terminal in this project folder.
2. Install the dependency:

	```bash
	pip install -r requirements.txt
	```

3. Run the program:

	```bash
	python main.py
	```

On some Windows systems, use `py main.py` instead.

## Controls

Press `Ctrl+C` in the terminal to stop the camera and restore the cursor.

## Settings

The main settings are near the top of `main.py`:

```python
WIDTH = 120
CAMERA_INDEX = 0
FPS = 30
```

- `WIDTH` controls the ASCII output width.
- `CAMERA_INDEX` selects the camera. Try `1` if the default camera cannot be opened.
- `FPS` controls the target frame rate.

## Troubleshooting

### The camera cannot be opened

- Check that another application is not using the webcam.
- Allow camera access for Python or your terminal in Windows privacy settings.
- Change `CAMERA_INDEX` from `0` to `1` or another available camera index.

### The output looks stretched

Terminal characters are usually taller than they are wide. Adjust the `WIDTH` value or change the aspect-ratio values in `frame_to_ascii()`.

### `ModuleNotFoundError: No module named 'cv2'`

Install the project dependency again:

```bash
pip install -r requirements.txt
```
