You are an engineer organizing a large multimedia project. Our primary source asset is a video file located at `/app/project_video.mp4`. Downstream microservices need rapid access to specific frames from this video to extract metadata.

Your task is to build a high-performance REST API and its corresponding test suite.

Step 1: API Construction & Data Encoding
Create a FastAPI application in `/home/user/app/server.py` that runs on `0.0.0.0:8000`.
It must have a single endpoint: `GET /api/v1/frame/{frame_number}` (where frame_number is a 0-indexed integer).
The endpoint must return a JSON response in this exact format:
```json
{
  "frame": 12,
  "data": "..." 
}
```
The `data` field must be the JPEG binary data of that specific frame from `/app/project_video.mp4`. However, to comply with our legacy ingestion system's idiosyncratic requirements, the JPEG binary must be Base64 encoded, and then the *entire Base64 string must be reversed* (e.g., if the base64 is `abc=`, the output must be `=cba`).

Step 2: Test Fixtures and Mocks
Write a test suite in `/home/user/app/test_server.py` using `pytest`. The test must verify the `/api/v1/frame/{frame_number}` endpoint without actually reading the video file. You must use `unittest.mock` to mock the video extraction logic so it returns a dummy 10x10 black JPEG image, and verify that the endpoint correctly applies the Base64-and-reverse encoding logic.

Step 3: Performance Optimization
Our production system requires high throughput. Spawning an `ffmpeg` process per request will result in terrible performance (e.g., 5-10 requests per second). You must optimize your server to achieve a high frame-serving throughput. The video is short (a few seconds long at 30 fps). You are strongly encouraged to perform initialization steps (like pre-extracting frames into memory or `/tmp`) when the server starts up so that subsequent requests are served instantly.

Start your server in the background using `uvicorn server:app --host 0.0.0.0 --port 8000` when you are done, so we can verify it. Write a log file to `/home/user/app/server_ready.log` containing the word "READY" when your server is fully initialized and ready to receive requests.

Constraints:
- Use Python 3.
- `ffmpeg` is preinstalled on the system.
- You can install any required pip packages (e.g., `fastapi`, `uvicorn`, `pytest`, `httpx`).