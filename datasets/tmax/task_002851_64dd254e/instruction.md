You are a deployment engineer tasked with rolling out an update for a legacy image-processing service. 

We need to deploy a new C-based HTTP service that reads an image file, performs OCR on it, and returns the result. You must set up the directory structure, write the C code, compile it, and expose it via an SSH tunnel.

Follow these steps exactly:

1. **Directory Structure & Configuration (Idempotent Setup)**
   Write a bash script at `/home/user/setup.sh` that idempotently creates the following structure:
   - `/home/user/app/releases/v2`
   - A symlink `/home/user/app/current` pointing to `/home/user/app/releases/v2`
   - A configuration file at `/home/user/app/current/config.txt` containing exactly one line: `IMAGE=/app/target_image.png`
   Run this script to ensure the filesystem is prepared.

2. **C HTTP Server**
   Write a C program at `/home/user/app/current/server.c` that does the following:
   - Starts a simple HTTP web server listening on `127.0.0.1` port `8080`.
   - Reads the image path from `/home/user/app/current/config.txt` (parsing the `IMAGE=` line).
   - When it receives an HTTP `GET /extract` request, it runs the `tesseract` command-line utility on the configured image path, directing the OCR output to stdout. (e.g., `tesseract /path/to/image stdout`).
   - Captures the stdout from tesseract and sends it back to the client as a `200 OK` HTTP response in plain text.
   - For any other endpoints, return a `404 Not Found`.

3. **Build and Run**
   Compile the C code to `/home/user/app/current/server` and start it in the background.

4. **SSH Tunneling**
   The service must be accessible on port `9090`. Since the server is bound to `127.0.0.1:8080`, establish a local port forward using SSH. Passwordless SSH to `user@localhost` is already configured on this system.
   Run an SSH command in the background that forwards local port `9090` to `127.0.0.1:8080`.

Ensure everything is running and the tunnel is active. The automated verifier will test the service by making an HTTP request.