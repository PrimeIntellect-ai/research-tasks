You are a machine learning engineer tasked with building a reproducible data processing and feature engineering pipeline for video data, and serving the engineered features via a REST API.

We have a source video located at `/app/dashcam.mp4`. 

Your goal is to extract frames from this video, compute specific numerical features, and serve them through an HTTP API. This will act as the feature extraction and validation step for a downstream anomaly detection model.

Please complete the following steps:

1. **Frame Extraction:**
   Use `ffmpeg` to extract frames from `/app/dashcam.mp4` at exactly 5 frames per second (FPS). Save the extracted frames as JPEG images in the directory `/home/user/frames`. Name them sequentially starting from 1 (e.g., `frame_1.jpg`, `frame_2.jpg`, etc.).

2. **Feature Engineering:**
   For each extracted frame (sorted by frame index), calculate the following:
   * `brightness`: The mean pixel intensity of the image after converting it to grayscale (using standard luminosity weights or simple averaging across RGB channels, but specify using OpenCV's standard `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` or PIL's `.convert('L')` for consistency).
   * `rolling_avg`: The moving average of the `brightness` for the last 3 frames (inclusive of the current frame). For frame 1, it's just frame 1's brightness. For frame 2, it's the average of frame 1 and 2. For frame 3 onwards, it's the average of the current and two preceding frames.
   * `is_flash`: A boolean feature that is `true` if the current frame's `brightness` is strictly greater than `1.5 * rolling_avg_of_previous_frame`. (For frame 1, `is_flash` is always `false`. For frame $N$, compare its brightness to the `rolling_avg` calculated at frame $N-1$).

3. **Feature Serving:**
   Create and start an HTTP REST API server listening exactly on `127.0.0.1:8080`.
   The API must have the following endpoint:
   * `GET /api/v1/frame/<frame_id>`

   Requirements for the API:
   * It must require an authorization header: `Authorization: Bearer secret-video-token`. If the header is missing or incorrect, return a `401 Unauthorized` status code.
   * If a valid `frame_id` (integer starting from 1) is requested, return a `200 OK` status code with the following JSON response format:
     ```json
     {
       "frame_id": 1,
       "brightness": 105.42,
       "rolling_avg": 105.42,
       "is_flash": false
     }
     ```
     (Round floating-point numbers to 2 decimal places in the JSON response).
   * If the `frame_id` exceeds the total number of extracted frames, return a `404 Not Found` status.

4. **Status Log:**
   Write a log file at `/home/user/pipeline_status.log` containing exactly one line: `Total frames processed: X` (where X is the integer number of frames extracted and processed).

Start your server in the background (e.g., using `nohup` or `&`) so that it remains running, and ensure the log file is written as requested. You may use any programming language (Python is recommended, utilizing Flask or FastAPI and standard data science libraries like `numpy` or `PIL`/`cv2`).