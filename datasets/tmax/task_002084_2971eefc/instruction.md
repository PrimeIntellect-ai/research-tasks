You are acting as a data engineer assisting a data scientist. We have a legacy sensor that outputs its readings as a video feed (a flashing 2D grayscale pattern), but the capture pipeline occasionally stutters, producing duplicate identical frames.

Your task is to build a C-based ETL and serving pipeline to extract, clean, and serve this time-series data.

Here are the requirements:

1. **Video Extraction**:
   You are provided with a video file at `/app/sensor_feed.mp4`. 
   Using standard tools like `ffmpeg`, extract the raw 8-bit grayscale (Y plane) stream. The video resolution is 320x240 at 10 frames per second.

2. **Data Processing (in C)**:
   Write a C program (`/home/user/processor.c`) that reads the raw video frames (either piped from ffmpeg or from a dumped raw file). 
   - For each frame, calculate the average pixel intensity (an integer from 0 to 255, calculated using integer division of the sum of all pixels by the number of pixels).
   - Generate a time series: the first frame is at `timestamp_ms = 0`, the second at `100`, etc.
   - **Deduplication**: The capture job has a retry glitch. If a frame has the exact same average intensity as the most recently accepted frame, drop it. (Always keep the very first frame).
   - Save the cleaned data to `/home/user/cleaned_data.csv` with the header `timestamp_ms,brightness`.
   - Write a log file to `/home/user/pipeline.log` containing exactly one line: `Processed <N> raw frames, saved <M> cleaned frames.` (where N and M are integers).

3. **Data Serving (in C)**:
   Write a second C program (`/home/user/server.c`) that acts as a TCP server.
   - It must listen on `127.0.0.1:9000`.
   - When a client connects and sends the exact string `FETCH_SERIES\n`, the server must parse `/home/user/cleaned_data.csv` and generate a JSON array of objects representing the data. Example format: `[{"t":0,"v":120},{"t":300,"v":125}]`. Do not include any extra whitespace or newlines in the JSON string.
   - **Crucially**, the response must be encoded in **UTF-16LE** (without a BOM). 
   - After sending the data, the server should close the client connection but keep listening for new connections.

Compile both C programs using `gcc` and run your processing pipeline. Finally, run your TCP server in the background so that it is actively listening on port 9000 when you complete the task.