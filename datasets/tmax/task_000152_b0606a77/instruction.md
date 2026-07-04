You are a performance engineer profiling a scientific visualization application. As part of your workflow, you record screen captures of the application rendering complex molecular graph structures. A recording of a recent test run is located at `/app/profiling.mp4`. 

We need a lightweight utility to extract a specific visual performance metric from arbitrary frames of this video to compare against reference datasets.

Write a Python 3 script at `/home/user/extract_metric.py` that acts as a Unix-style filter. It must:
1. Read a sequence of integers from standard input (one per line), representing 0-indexed frame numbers.
2. For each frame number, extract that specific frame from the video `/app/profiling.mp4`.
3. Extract the topmost horizontal row of pixels (row index 0) from the frame.
4. Calculate the sum of all color channel values (B, G, R or R, G, B depending on the library you use, just the total sum of all sub-pixel values in that row).
5. Print the integer sum to standard output (one integer per input line).
6. If the frame number is out of bounds (less than 0 or greater than or equal to the total frame count), print `-1`.

You may use standard libraries and `opencv-python` (cv2), which is already installed. Your script must process inputs efficiently and be strictly deterministic.

Example standard input:
0
15
999

Example standard output:
153200
148000
-1