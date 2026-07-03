**IT Support Ticket: #INC-89221 - Video Diagnostic Service Down**

Hello,

Our engineering team deployed a new internal Go microservice designed to extract specific diagnostic frames from video feeds, but it's currently failing all integration tests. The service source code is located at `/home/user/workspace/vid_service/`. 

The service is supposed to expose a REST API that accepts a JSON payload to extract `n` frames from a given video file. However, it has several critical bugs:

1. **Formula Implementation Error**: The API receives `t0` (start time in seconds), `delta` (time multiplier), and `n` (number of frames). The timestamps to extract should be calculated as exactly: `T_i = t0 + (i * i * delta)` for `i` from `0` to `n-1`. The current code is calculating this incorrectly.
2. **Encoding/Serialization Issues**: The HTTP response is supposed to return a JSON object with a single field `frames` containing an array of Base64-encoded JPEG strings. Currently, the JSON is either returning empty fields or crashing due to improper Go struct visibility and incorrect base64 encoding.
3. **Extraction Bug**: The `ffmpeg` wrapper command inside the Go code is failing to capture the exact frame as a JPEG image.

Your task:
1. Fix the Go code in `/home/user/workspace/vid_service/main.go`.
2. Ensure the `ffmpeg` command correctly seeks to the exact timestamp `T_i` and captures exactly 1 frame as a JPEG.
3. Fix the JSON serialization so the HTTP response perfectly matches the required schema.
4. Build and start the Go service. It MUST listen on `0.0.0.0:8080`.
5. Keep the service running in the background.

There is a test video located at `/app/diagnostic_feed.mp4`. We will run an automated verifier against your service using this video once you have it running.

**Expected Request Format:**
`POST /extract`
```json
{
  "video_path": "/app/diagnostic_feed.mp4",
  "t0": 1.5,
  "delta": 0.5,
  "n": 3
}
```

**Expected Response Format:**
HTTP 200 OK
```json
{
  "frames": [
    "<base64_string_of_frame_at_1.5s>",
    "<base64_string_of_frame_at_2.0s>",
    "<base64_string_of_frame_at_3.5s>"
  ]
}
```

Please resolve these bugs and leave the fixed service running on port 8080.