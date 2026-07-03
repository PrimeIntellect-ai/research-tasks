As a backup administrator, you are tasked with archiving a set of media assets and exposing them via a specialized Media Backup REST API.

Your target data is located in `/app/media_assets`. You must write a Python-based HTTP server to index and serve this data. 
Beware: The directory contains poorly configured symbolic links that create infinite recursive loops. Your backup indexing logic must traverse the directory recursively, calculate checksums, and carefully track visited real paths to avoid getting stuck in an infinite loop.

Develop a Python HTTP server that runs continuously on `127.0.0.1:8080`. 

Your server must implement the following specification:
1. **Authentication**: All endpoints must require an `Authorization` header with the exact value: `Bearer backup_token_2024`. If missing or invalid, return a `401 Unauthorized` status.
2. **Endpoint `GET /manifest`**: 
   - Recursively traverse `/app/media_assets`.
   - Calculate the SHA-256 checksum for every valid regular file.
   - Ignore any directories or files that lead to an infinite symlink loop (do not follow a symlink if its real path has already been visited in the current branch).
   - Return a JSON object with `200 OK` where keys are the relative file paths (e.g., `logs/system.log` or `video/surveillance.mp4`) and values are the corresponding SHA-256 hex digests.
3. **Endpoint `GET /thumbnail`**:
   - The directory contains a video file: `/app/media_assets/surveillance.mp4`.
   - Using `ffmpeg` (which is pre-installed) and standard stream redirection/piping (do not create temporary files on disk), extract the video frame at exactly 00:00:05.000 (5 seconds).
   - The frame must be encoded as a PNG.
   - Return the raw PNG binary data as the response body with `Content-Type: image/png` and a `200 OK` status.

Requirements:
- Your script must be written in Python.
- Use built-in Python libraries for the HTTP server (`http.server` or similar) or install lightweight frameworks like `Flask` or `FastAPI` if you prefer.
- Start the server in the background so it is actively listening on `127.0.0.1:8080` when you consider the task complete. Keep it running!
- Ensure your directory traversal properly identifies and skips cyclical symlinks while still including valid symlinked files.