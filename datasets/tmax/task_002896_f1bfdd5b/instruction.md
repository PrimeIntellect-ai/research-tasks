You are acting as a container specialist managing a new microservice architecture that handles edge-device video feeds and payload configurations. We need to set up the environment, process an initial video artifact, build a sanitization pipeline for incoming configuration payloads, and prepare the filesystem and reverse proxy routing.

Complete the following tasks:

1. **Video Artifact Processing**
   There is a raw video feed from an edge security camera located at `/app/security_cam.mp4`. Use `ffmpeg` or `ffprobe` (which are preinstalled) to determine the exact number of frames in this video. 
   Save this integer value to `/home/user/frame_count.txt`.

2. **Environment Variable & Shell Profile Setup**
   Modify `/home/user/.profile` to export the following environment variables:
   - `PROXY_UPSTREAM=127.0.0.1:8080`
   - `VIDEO_PROCESSED_COUNT=<the_frame_count_from_step_1>`

3. **Adversarial Payload Sanitizer**
   Our microservices receive JSON configuration payloads that specify directories to mount. However, some payloads are malicious and attempt path traversal.
   Write a Python or multi-language script at `/home/user/filter_payloads.py` with the following CLI signature:
   `python3 /home/user/filter_payloads.py <input_dir> <output_dir>`
   
   The script must read all `.json` files in `<input_dir>`. A JSON file is considered "clean" if the value of its `"mount_path"` key does NOT contain the substring `../`. If it contains `../`, it is "evil".
   The script must copy ALL "clean" JSON files to `<output_dir>` without modifying them, and completely ignore/reject the "evil" ones.

4. **Mount & fstab Configuration**
   Assume you have run your filter script on a set of payloads, and the clean ones are now in `/home/user/accepted_payloads/` (you will need to create this directory and run your script against the payloads I provide in the environment). 
   For every clean payload in `/home/user/accepted_payloads/`, extract the `"mount_path"` value. Generate a pseudo-fstab file at `/home/user/container_fstab` containing one line per clean payload in the following format:
   `tmpfs <mount_path> tmpfs defaults 0 0`

5. **Reverse Proxy Setup**
   Create a local Nginx configuration file at `/home/user/nginx.conf`. It should:
   - Run in the foreground or as a user-level process (no daemon, `pid /home/user/nginx.pid;`).
   - Listen on port `9090`.
   - Proxy all HTTP requests to the upstream defined in your `.profile` (`http://127.0.0.1:8080`).
   - Only proxy the request if the HTTP header `X-Microservice: accepted` is present. If the header is missing or has a different value, return a `403 Forbidden` status code.

Ensure all files are created exactly at the specified paths. Do not start the Nginx server; simply leave the valid configuration file at `/home/user/nginx.conf`.