You are tasked with fixing a broken web service architecture and implementing a video analysis pipeline.

Currently, there is a requirement to deploy a secure backend API that analyzes a security feed, but the configuration is incomplete and insecure. You must act as a systems engineer to build and harden this setup entirely within the `/home/user/` directory (you do not have root access).

Here is what you need to do:

1. **Video Processing & Backend API (Python)**
   Write a Python web backend (using Flask, FastAPI, or any similar framework) that listens on a Unix socket at `/home/user/backend.sock`.
   The application must have an endpoint `GET /api/anomaly`. When called, it should analyze the provided video fixture located at `/app/anomaly_feed.mp4`. 
   The video contains exactly one frame that is entirely solid red (RGB: 255, 0, 0). 
   The `/api/anomaly` endpoint must compute and return a JSON payload with the 0-indexed frame number of this anomaly:
   `{"anomaly_frame": <int>}`
   Additionally, your application or a separate script must extract all frames as JPEG images into `/home/user/extracted_frames/` (e.g., named `frame_0000.jpg`, `frame_0001.jpg`, etc.).

2. **Directory & Link Management**
   Create a directory `/home/user/web_root/`. Inside it, create a symlink named `media` that points to `/home/user/extracted_frames/`.

3. **Reverse Proxy (Nginx)**
   Create a custom Nginx configuration file at `/home/user/nginx.conf`. 
   The Nginx server must:
   - Run as an unprivileged user (set necessary paths for pid, temp directories, etc. to `/home/user/nginx_temp/` so it runs without root).
   - Listen on `127.0.0.1:8080`.
   - Route requests for `/static/` to serve files from the symlink `/home/user/web_root/media/`. (e.g., `/static/frame_0142.jpg` should serve the extracted frame).
   - Route requests for `/api/` to the Python backend via the Unix socket `/home/user/backend.sock`.
   - **Hardening:** The `/api/` route must be protected. Nginx must reject any request to `/api/` that does not include the HTTP header `Authorization: Bearer syseng-secure-2024` with a `403 Forbidden` status. 

4. **Service Management**
   Ensure both your Python backend (using a WSGI/ASGI server like Gunicorn/Uvicorn) and the Nginx server (using `nginx -c /home/user/nginx.conf`) are running in the background.

Once you have written the code, extracted the frames, created the configuration, and started the background processes, the automated verifier will test your Nginx endpoint at `127.0.0.1:8080`.