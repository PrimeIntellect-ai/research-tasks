We experienced a major system outage yesterday where our local Nginx gateway started returning 502 Bad Gateway errors. We need you to investigate the incident, fix the gateway configuration, and implement a detection mechanism for the malicious traffic that caused the underlying service crash.

You must complete the following tasks:

1. **Incident Video Analysis:**
   We captured a screencast of our monitoring dashboard during the outage, located at `/app/incident.mp4`. The dashboard is solid green during normal operation, but turns solid red (`#FF0000`) during the 502 outage. 
   Using Python and `ffmpeg` (which is preinstalled), extract and analyze the frames to find the exact 0-indexed frame number where the first red frame appears. 
   Write this frame number as a single integer to `/home/user/incident_frame.txt`.

2. **Fix Nginx Configuration:**
   Our Nginx config is version-controlled in a local git repository at `/home/user/gateway`. The configuration file is `nginx.conf`. 
   Currently, it is misconfigured and pointing to a dead upstream port, causing the 502 errors. Update `nginx.conf` so that the `proxy_pass` directive points to the correct upstream application running at `http://127.0.0.1:8081`. 

3. **Develop a Malicious Traffic Classifier:**
   The upstream Python application crashed because it couldn't handle path traversal attacks. You must write a Python script at `/home/user/classifier.py` that detects these malicious requests.
   - The script must accept exactly one command-line argument: the path to a file containing a raw HTTP request.
   - It must read the file and analyze the HTTP request path.
   - If the path contains `../` or URL-encoded equivalents like `%2e%2e` or `%2E%2E` (case-insensitive), it must print `EVIL` to stdout and exit with status code 1.
   - Otherwise, it must print `CLEAN` to stdout and exit with status code 0.
   - Your classifier will be tested against two hidden corpora of requests to verify its accuracy.

4. **CI/CD Git Hook Configuration:**
   To prevent bad test requests from being committed in the future, navigate to the `/home/user/gateway` git repository and create a `pre-commit` git hook (`.git/hooks/pre-commit`). 
   The hook must:
   - Use text processing (e.g., `git diff`, `awk`, `grep`) to find all `.req` files that are currently staged for commit.
   - Run your `/home/user/classifier.py` on each staged `.req` file.
   - If the classifier exits with code 1 (EVIL) for any file, the hook must block the commit by exiting with a non-zero status.
   - Make sure the hook is executable.

Ensure all files are created with the correct permissions and run as the standard `user`. Do not use `sudo`.