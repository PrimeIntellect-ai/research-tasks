You are tasked with building a configuration management tracking service. Your goal is to write a Python-based HTTP server that receives configuration updates in a compressed package, replays a custom Write-Ahead Log (WAL) to apply changes, hashes the resulting state using a proprietary binary, and returns the packaged results.

Here are the exact requirements:

1. **Service Endpoint & Protocol:**
   Create an HTTP server listening on `0.0.0.0:8000`.
   It must expose a single endpoint: `POST /process_config`.
   The request body will be the raw bytes of a ZIP archive.
   The service must process the archive and respond with an `application/zip` payload containing the final state.

2. **Archive Extraction & Parsing:**
   The uploaded ZIP archive will contain arbitrary configuration files and exactly one log file named `update.wal`.
   Extract the archive to a temporary workspace.
   Parse and execute `update.wal`. The WAL file is a plain-text file where each line represents an operation separated by pipes (`|`).
   Format: `COMMAND|FILENAME|PAYLOAD`
   Commands you must support:
   - `CREATE|filename|base64_data`: Create a new file with the decoded base64 payload. If it exists, overwrite it.
   - `APPEND|filename|base64_data`: Append the decoded base64 payload to the existing file. If it doesn't exist, ignore the command.
   - `DELETE|filename|none`: Delete the file. The payload field will be the literal string "none".

3. **Proprietary Hashing:**
   There is a stripped, black-box binary located at `/app/config_hasher`. 
   After applying all operations from the WAL file, you must hash every remaining file in the workspace (excluding `update.wal` itself).
   To hash a file, execute `/app/config_hasher <absolute_path_to_file>`. The binary writes the proprietary hash to stdout.
   Create a file named `hashes.txt` in the root of the workspace.
   For each file (sorted alphabetically by their relative paths in the workspace), write a line to `hashes.txt` in this exact format:
   `relative/path/to/file: <stdout_from_hasher>`
   (Note: strip any trailing newlines from the hasher's output on each line).

4. **Response:**
   Delete `update.wal` from the workspace.
   Create a new ZIP archive containing the modified configuration files and the newly generated `hashes.txt`.
   The paths inside the ZIP must be relative to the root of the workspace (i.e., `hashes.txt` should be at the root of the ZIP).
   Return the raw bytes of this new ZIP archive as the HTTP response with a 200 OK status code.

Ensure your server runs continuously and handles multiple sequential requests. You may use standard library modules (e.g., `http.server`, `zipfile`, `base64`, `subprocess`, `tempfile`).