You are tasked with building a Secure Artifact Curation Server in Go. As an artifact manager, we often receive binary repositories (archives) from untrusted sources. Some of these archives are poorly constructed or intentionally malicious, containing infinite symlink loops designed to break backup scripts and scanners. Additionally, we receive out-of-band audio transmissions that contain authorization passphrases required for curation.

Your objective is to write a Go service that safely scans an untrusted archive, transcribes an audio file, and serves the results over a specific HTTP API.

Here are the requirements:

1. **Audio Transcription**: 
   There is an audio artifact located at `/app/transmission.wav`. It contains a short spoken English passphrase. 
   You must transcribe this audio file. You may use any available terminal tools, Python packages (e.g., `openai-whisper`), or external transcription utilities you can install in the environment to recover the spoken text.

2. **Safe Archive Scanning**:
   There is an untrusted archive located at `/app/artifacts.tar`.
   This archive contains regular files, directories, and symlinks. However, it also contains malicious infinite symlink loops (e.g., a symlink pointing to its own parent directory).
   Your Go application must parse the `.tar` file directly (using Go's `archive/tar`, streaming or memory-mapped) *without* extracting it to the filesystem.
   It must simulate a directory traversal of the archive's contents, recording the absolute paths of all valid, non-looping regular files. If a symlink creates a cycle (visiting the same logical directory path twice via symlink resolution), your parser must detect the loop, skip that branch, and avoid getting stuck in an infinite loop.

3. **HTTP API**:
   Your Go service must start an HTTP server listening on `127.0.0.1:8080`.
   It must expose the following endpoints:
   
   - `GET /status`
     Must return a `200 OK` with the JSON response: `{"status": "ready"}`
     
   - `POST /curate`
     Must require an `Authorization: Bearer <TRANSCRIPT>` header, where `<TRANSCRIPT>` is the exact lowercase text transcribed from `/app/transmission.wav` (stripped of punctuation and leading/trailing whitespace).
     If the token is missing or incorrect, return `401 Unauthorized`.
     If the token is correct, return a `200 OK` with a JSON body containing the list of valid regular file paths found in `/app/artifacts.tar`, formatted like so:
     ```json
     {
       "valid_files": [
         "/readme.txt",
         "/bin/data.csv",
         "/config/settings.xml"
       ]
     }
     ```
     *(Note: The paths must be normalized to start with a `/`, representing the root of the archive).*

Start the Go server in the background and leave it running so that the automated test suite can verify its endpoints. Write your code in `/home/user/curator/main.go`.