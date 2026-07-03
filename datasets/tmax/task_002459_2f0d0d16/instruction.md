You are an edge computing engineer deploying an inference and telemetry pipeline to a fleet of Linux-based IoT devices. You need to configure a local processing pipeline on this node.

There are four parts to this deployment:

1. **Fix the Frame Extractor (Cron/Filesystem Anchor)**
There is a video file located at `/app/video.mp4`. A script at `/home/user/edge_deploy/extract.sh` is scheduled via a user cron job to extract frames from this video using `ffmpeg` (1 frame per second). 
However, when the cron job runs, it fails to find `ffmpeg` or dumps the output frames into `/tmp/` instead of the expected persistent storage at `/home/user/frames/` due to environment and PATH differences. 
Fix the `/home/user/edge_deploy/extract.sh` script and the user crontab so that when cron executes it, exactly the correct number of frames are extracted as `.jpg` files into `/home/user/frames/`.

2. **Telemetry Sanitizer (Adversarial Corpus)**
IoT sensors generate telemetry payloads, but occasionally spoofed or malformed data enters the stream. 
Write a multi-language filter (e.g., a Python script `sanitizer.py` wrapped by a shell pipeline, or vice versa) located at `/home/user/edge_deploy/sanitizer.py`.
The script must accept a single file path as a command-line argument. It should read the file and determine if the telemetry is valid.
Valid telemetry (clean) consists of a JSON object with a `"sensor_id"` (string starting with "CAM-"), a `"timestamp"` (integer), and `"status"` (strictly the string "OK").
Any file missing these fields, containing extra unexpected fields, having a `"status"` other than "OK", or being invalid JSON is considered "evil".
The script MUST exit with code `0` for clean files, and exit with code `1` for evil files. Do not output anything to stdout.

3. **Backend Service (Container Lifecycle)**
Start two background web servers (you can use `python3 -m http.server` or rootless podman/docker containers) serving the `/home/user/frames/` directory. They must run on `127.0.0.1:9001` and `127.0.0.1:9002`.

4. **Edge Load Balancer (Reverse Proxy)**
Configure and run a local instance of `haproxy` or `nginx` (running as the standard `user`, without root privileges) that listens on `127.0.0.1:8080`. It must act as a round-robin load balancer forwarding requests to the two backend web servers created in step 3. Write its configuration file to `/home/user/edge_deploy/lb.conf`.

Ensure all services are running and the scripts are correctly placed.