You are an engineer tasked with curating binary repositories for a new artifact manager. Your system has received an audio memo from the infrastructure team and a raw, tangled directory of legacy artifact repositories.

You must complete the following steps to clean up the environment and expose the configuration via a Go-based API:

1. **Extract Audio Data:**
   There is an audio file at `/app/artifact_memo.wav`. Transcribe this file using any available tool (e.g., `whisper` or `ffmpeg` to process). The audio dictates a configuration sentence containing a critical master server IP address (e.g., "The new master server IP is X.X.X.X").
   Use standard CLI tools (`sed`, `awk`, `grep`) to parse the transcription, extract ONLY the IPv4 address, and redirect it into `/home/user/master_ip.txt`.

2. **Untangle the Repository:**
   The legacy artifact directory is located at `/home/user/repo_data/`. Due to a poorly written backup script, there is an infinite symlink loop within this directory structure that causes standard traversal tools to crash or hang indefinitely. 
   Find the symlink that creates this infinite loop and remove it. Keep all other valid files, directories, and non-looping symlinks intact. Count the exact number of *regular files* (ignoring directories and symlinks) remaining in `/home/user/repo_data/` and its subdirectories.

3. **Build the API Service (Go):**
   Write and run a Go HTTP server located at `/home/user/server.go`.
   The server must listen on `0.0.0.0:8080` and expose a single endpoint:
   - `GET /api/status`
   
   The endpoint must return a JSON payload with a `200 OK` status in the exact following format:
   ```json
   {
     "master_ip": "<IP_EXTRACTED_FROM_AUDIO>",
     "artifact_count": <INTEGER_COUNT_OF_REGULAR_FILES>
   }
   ```

Ensure your Go server is running in the background and listening on port 8080 before you finish. Do not use external Go libraries outside the standard library for the HTTP server.