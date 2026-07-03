You are the site administrator for a platform that requires users to upload video verifications to create accounts. Recently, malicious actors have been spoofing the verification process. We have noticed that the spoofing software they use leaves a subtle artifact: a pure red square (RGB: 255, 0, 0) of exactly 10x10 pixels in the absolute top-left corner (coordinates x:0-9, y:0-9) of at least one frame in the video.

Your task is to build a robust automated video filtering pipeline and secure its API proxy.

Step 1: Video Filter Script
Write a Python script at `/home/user/filter_video.py`. The script must take a single command-line argument: the absolute path to an MP4 video file.
- It must extract and examine the frames of the video (you can use `ffmpeg`, `opencv-python`, or `Pillow`).
- If ANY frame contains the 10x10 pure red spoofing artifact in the top-left corner, the script must immediately terminate with exit code 1 (indicating a rejected/evil video).
- If all frames are clean, the script must terminate with exit code 0 (indicating an accepted/clean video).
Robust error handling should be included if the file is missing or corrupt.

Step 2: Incident Analysis
We have captured a video of a confirmed spoofing attempt at `/app/incident_record.mp4`. Use your script or custom logic to find the exact frame number (0-indexed) where the red artifact first appears. Write only this integer frame number into `/home/user/incident_report.txt`.

Step 3: Secure Service Proxy (User-Space Firewall & Port Forwarding)
We plan to wrap your script in an API listening on port 8081. You must set up an Nginx reverse proxy to protect it.
Create an Nginx configuration file at `/home/user/proxy.conf` that:
- Runs as the current unprivileged user.
- Listens on port 8080.
- Forwards all traffic to `127.0.0.1:8081`.
- Acts as a firewall by ONLY allowing requests from the IP `127.0.0.1`. It must deny requests from any other IP address (returning a 403 Forbidden).

Ensure that your `filter_video.py` is accurate, as it will be rigorously tested against our internal database of clean and evil videos.