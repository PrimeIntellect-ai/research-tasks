You are a Data Engineer building an automated ETL and analysis pipeline for video feeds using Go. 

We have a surveillance video file located at `/app/video.mp4`. Your task is to process this video to detect motion events, track the effects of different sensitivity thresholds, and serve the extracted events via a REST API.

Step 1: Extract (Data Ingestion)
Use `ffmpeg` (which is pre-installed) to extract frames from `/app/video.mp4`. 
- Extract the frames at exactly 1 frame per second (fps).
- Convert the frames to grayscale.
- Save them as PNG files in `/tmp/frames/` with the naming convention `frame_0001.png`, `frame_0002.png`, etc.

Step 2: Transform (Linear Algebra & Analysis)
Write a Go program to calculate the Average Pixel Difference (APD) between consecutive frames. 
- Treat each grayscale image as a 2D matrix of 8-bit unsigned integers (0-255).
- For consecutive frames $F_{t-1}$ and $F_t$ (e.g., `frame_0001.png` and `frame_0002.png`), compute the absolute difference for each corresponding pixel.
- The APD is the sum of these absolute differences divided by the total number of pixels in the frame.
- An "event" occurs at frame $t$ (the second frame in the pair) if the APD between $F_{t-1}$ and $F_t$ is strictly greater than a given threshold $T$. Frame indices start at 1. The first possible event is at frame 2.

Step 3: Experiment Tracking
Run your Go analysis for thresholds $T \in \{5, 10, 15, 20\}$. 
Log the total number of events detected for each threshold into an experiment tracking file at `/home/user/experiments.jsonl`.
Each line must be a valid JSON object with exactly these keys:
`{"threshold": 5, "event_count": 12}` (where 12 is an example count).

Step 4: Load (Serving the Data)
Extend your Go program to run as an HTTP server that serves the computed event data.
- The server must listen on `127.0.0.1:9090`.
- It must expose a `GET /api/events` endpoint.
- The endpoint must accept a `threshold` query parameter (e.g., `?threshold=10`) which can be any float value.
- The endpoint must dynamically return a JSON response containing the list of frame numbers (integers) where an event occurred for that threshold: `{"events": [2, 5, 8]}`.
- **Authentication:** All requests to the server will include the header `X-API-Key: etl-golang-video`. If this header is missing or incorrect, return a 401 Unauthorized status code.

Leave the HTTP server running in the background so it can be verified. Keep your Go code at `/home/user/pipeline.go`.