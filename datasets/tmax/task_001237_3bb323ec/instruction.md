You are a storage administrator managing disk space on a critical server. You need to write a Go HTTP service that automates the cleanup of corrupt archives, parses storage logs, and extracts diagnostic frames from a video artifact.

Your task is to write and run a Go web server listening on `127.0.0.1:8080`. The server must implement the following endpoints:

1. `GET /status`
   - Returns a 200 OK with JSON `{"status": "ok"}`.

2. `POST /archives/clean`
   - Reads the configuration file `/home/user/config.yaml`. This file contains a YAML list under the key `prefixes` (e.g., `prefixes: ["db_", "app_"]`).
   - Scans the directory `/home/user/archives/` for `.tar.gz` files.
   - Verifies the integrity of each archive (e.g., ensuring it can be successfully decompressed and listed without errors).
   - Deletes any `.tar.gz` files that are corrupt.
   - Returns a JSON array of the filenames (just the base names) of all valid, uncorrupted archives whose names start with one of the prefixes specified in the config.

3. `GET /logs/errors`
   - Parses the multi-line log file `/home/user/storage.wal`. Each log entry starts with a timestamp `YYYY-MM-DD HH:MM:SS`. Error entries contain the word `ERROR` followed by a unique `ErrID: <UUID>` on a subsequent line before the next timestamp.
   - Returns a plain text integer representing the total count of unique `ErrID`s found in the file.

4. `POST /video/extract`
   - Uses `ffmpeg` (or any appropriate tool) to extract a single frame from the diagnostic video `/app/storage_scan.mp4` at exactly the 00:00:05 mark.
   - Saves the frame as `/home/user/frame.jpg`.
   - Creates a standard zip archive at `/home/user/frame.zip` containing ONLY the `frame.jpg` file (no directories).
   - Returns the SHA256 checksum of the resulting `frame.zip` file as plain text.

Ensure your Go server remains running in the background so it can be evaluated by our automated testing suite. You may use any standard shell tools alongside your Go code.