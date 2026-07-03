You are a Linux Systems Engineer responsible for hardening a new video surveillance backend. 

A dashcam video file has been deposited at `/app/dashcam.mp4`. Your objective is to create a secure, robust Python-based API service that extracts and hashes specific frames from this video, alongside an idempotent deployment script. 

Since you do not have root access, you will configure this as a user-space daemon listening on a high port.

Here are your exact requirements:

1. **Filesystem Preparation:**
   Create an idempotent bash script named `/home/user/setup_fs.sh`. When executed, this script must safely create the directory `/home/user/frame_cache` if it does not exist, and aggressively enforce its permissions to `0700`.

2. **The Python API Service:**
   Write a Python web server (you may use standard libraries or `pip install flask`/`fastapi` as you prefer) in `/home/user/video_api.py`.
   - The service must bind to `127.0.0.1` on port `9090`.
   - **Endpoint 1:** `GET /health` 
     Must return an HTTP 200 with the JSON payload: `{"status": "running"}`. This endpoint must be public.
   - **Endpoint 2:** `GET /frame_hash`
     Must be protected. If the request does not include the exact HTTP header `Authorization: Bearer vault-key-2024`, it must return an HTTP 401 Unauthorized.
     If authorized, the service must execute `ffmpeg` to extract exactly 1 frame at the `00:00:12` mark of `/app/dashcam.mp4`. 
     *Mandatory ffmpeg arguments to ensure consistent hashing:* 
     `ffmpeg -y -ss 00:00:12 -i /app/dashcam.mp4 -vframes 1 -q:v 2 /home/user/frame_cache/frame_12.jpg`
     Once extracted, calculate the SHA-256 checksum of the resulting `frame_12.jpg` file. The endpoint must return an HTTP 200 with the JSON payload: `{"hash": "<the_sha256_hex_digest>"}`.
   - Implement robust error handling (e.g., returning HTTP 500 if the video file is missing or `ffmpeg` fails).

3. **Service Management:**
   Write an idempotent launch script `/home/user/launch.sh`. This script should:
   - Run `/home/user/setup_fs.sh`.
   - Install any Python dependencies you chose to use.
   - Check if the service on port 9090 is already running. If it is, do nothing. If it is not, start `/home/user/video_api.py` in the background, logging standard output and error to `/home/user/api.log`.

Execute `/home/user/launch.sh` so the service is actively running and listening on `127.0.0.1:9090` when you complete the task.