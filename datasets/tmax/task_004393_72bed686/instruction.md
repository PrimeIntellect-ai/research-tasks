You are an AI assistant helping a researcher organize and expose datasets.

The researcher has a collection of dataset archives and needs an automated way to verify them, generate manifests, and serve these manifests over an HTTP API. 

We have provided a vendored package for directory watching at `/app/watchdog-3.0.0`. However, the researcher reported that installing and running it fails due to a deliberate bug introduced by a previous lab member.

Your task is to:
1. Fix the bug in the vendored `/app/watchdog-3.0.0` package and install it in the current environment.
2. Write a Python script `/home/user/dataset_server.py` and run it in the background. The script must:
   - Monitor the directory `/home/user/datasets/incoming/` (create it if it doesn't exist) for new `.zip` files using the `watchdog` library.
   - When a new `.zip` file is detected, verify its archive integrity.
   - Generate a manifest mapping every file path inside the zip archive to its SHA-256 checksum.
   - Start an HTTP server listening on `127.0.0.1:8888`.
   - Expose an endpoint `GET /manifest?archive=<filename>` (e.g., `/manifest?archive=data.zip`). If the archive has been processed and is valid, return a JSON response with status code 200, where the keys are the internal file paths and values are the SHA-256 hex digests. If the archive is invalid or hasn't been processed, return a 404 status code.

Make sure to start your server script in the background so it is actively listening on port 8888 when you complete your task.