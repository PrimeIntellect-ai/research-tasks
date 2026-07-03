I need you to build a time-series extraction and processing pipeline for an automated monitoring system. 

We have a screen recording of a legacy server's debug console, provided as a video file at `/app/server_logs.mp4`. The video is exactly 60 seconds long at 1 FPS. Every second, the console prints a new line containing system metrics in a raw, unstructured, and sometimes noisy text format. 

A typical line on the screen looks something like this:
`[DEBUG] seq: 004 | CPU_USAGE: 45.2% | RAM: 1024M`

Your objective is to build a Python-based pipeline (`/home/user/pipeline.py`) that orchestrates the following tasks:
1. **Frame Extraction**: Extract exactly 1 frame per second from the video.
2. **OCR & Tokenization**: Read the text from each frame. Tokenize the resulting string to isolate the CPU usage numerical value. Note: OCR can be noisy (e.g., confusing `O` with `0`, adding extra spaces, or garbling the `%` sign). You must implement a normalization step to robustly parse the float value of the CPU usage.
3. **Windowed Aggregation**: Reconstruct this data into a time series. Use Pandas to compute a 5-second trailing rolling average of the CPU usage (e.g., the smoothed value at $t=5$ is the average of $t=1, 2, 3, 4, 5$). For the first 4 seconds, just average the available data.
4. **Output**: Save the final smoothed time series to `/home/user/smoothed_cpu.csv`. The CSV must have exactly two columns: `second` (integer, 1 to 60) and `smoothed_cpu` (float).

You must write a master Python script `/home/user/pipeline.py` that executes this entire workflow (the DAG) end-to-end. You can use `ffmpeg` via subprocess for frame extraction, and `pytesseract` / `cv2` for OCR.

Please execute your pipeline so that the output CSV is created. Your solution will be evaluated based on the Mean Squared Error (MSE) between your smoothed time series and the hidden ground-truth signal.