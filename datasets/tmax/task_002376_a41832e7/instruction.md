You are tasked with fixing and completing a Go-based REST API service that handles software patch validation and processes a video artefact.

You have been given a Go project in `/app/patch-api`. Currently, it fails to build due to a circular import between the `router` package and the `handlers` package. 

Your objectives are:
1. **Fix the Go Project**: Refactor the code in `/app/patch-api` to resolve the circular import. The project must compile successfully (`go build`) and start a REST API server.
2. **Implement Patch Validation**: The API has an endpoint `POST /api/v1/patch` that accepts a unified diff (patch) as its raw body. You must implement the validation logic for this endpoint. A patch is considered "malicious" (evil) if any of the file paths in the `+++` or `---` diff headers contain directory traversal sequences (e.g., `../`) or are absolute paths (e.g., `/etc/passwd`). The endpoint must return an HTTP 400 Bad Request if the patch is malicious, and an HTTP 200 OK if the patch is safe. Ensure your server is running in the background on port 8080.
3. **Video Processing**: There is an incident recording located at `/app/incident.mp4`. You need to extract frames from this video at a rate of 1 frame per second. After extracting the frames to a directory of your choice, count the total number of extracted frames and write this integer to `/app/frame_count.txt`.

Ensure the API is robust and correctly handles edge cases in diff formatting. Do not use external Go libraries for the diff parsing; use standard library string and routing functions.