Our video processing proxy is currently down, returning a 502 Bad Gateway to clients. We need you to fix the deployment structure, implement a request filter to prevent the backend from crashing, and configure log rotation.

You do not have root access. All services must be run under the `user` account.

Here are your objectives:

1. **Deployment Structure & Symlinks:**
   The deployment directory `/home/user/deployment/` is currently disorganized. We use a rolling deployment structure.
   - Create the directories `/home/user/deployment/releases/v1.0.0/` and `/home/user/deployment/releases/v2.0.0/`.
   - Set up `/home/user/deployment/current` as a symbolic link pointing to the `v2.0.0` release directory.

2. **Video Analysis & The Filter Script:**
   The backend crashes (causing the 502) when it receives malicious payloads or requests for frames that do not exist in our source video. We have a test video located at `/app/test_video.mp4`.
   You must write a request validator script at `/home/user/deployment/current/filter.py` that takes a single file path as a command-line argument. The file will contain a JSON payload like `{"frame": 120, "callback": "https://example.com/webhook"}`.
   
   Your `filter.py` script must:
   - Extract the total number of frames from `/app/test_video.mp4` (you can use `ffmpeg` or `ffprobe`).
   - Read the JSON file provided as the argument.
   - **Accept (exit code 0):** If the requested `frame` index is less than or equal to the total number of frames in the video, AND the `callback` URL is safe (contains ONLY alphanumeric characters and any of these: `:`, `/`, `.`, `?`, `=`, `-`, `_`).
   - **Reject (exit code 1 or higher):** If the `frame` index exceeds the total frames of the video, OR the `callback` URL contains any other characters (e.g., shell metacharacters like `;`, `$`, `|`, `&`, space, etc.).

3. **Log Rotation:**
   Create a bash script at `/home/user/deployment/current/rotate.sh`. When executed, it should look at `/home/user/logs/access.log`. It should rename the current `access.log` to `access.log.<timestamp>` (using Unix epoch time), create a new empty `access.log`, and ensure that NO MORE than 3 archived log files exist in the `/home/user/logs/` directory at any given time (delete the oldest ones).

4. **Integration Validation:**
   Ensure your `filter.py` is executable and works perfectly. We will test it against a corpus of requests. You can test your own logic to ensure you are properly validating the frame bounds and URL characters.