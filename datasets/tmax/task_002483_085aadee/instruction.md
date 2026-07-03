I need your help organizing some legacy project files and exposing their metadata via a local web service. This is a multi-step process.

First, there is a custom binary archive located at `/app/project_archive.bin`. You need to parse this file and extract its contents. The binary format is as follows:
- A 6-byte header: the ASCII string "PROJ" followed by 2 bytes representing the version (which will be `0x01` `0x00`).
- This is followed by a sequence of file records. Each record consists of:
  - A 2-byte unsigned short (little-endian) indicating the length of the file path.
  - The file path as an ASCII string.
  - A 4-byte unsigned integer (little-endian) indicating the size of the file data in bytes.
  - The raw file data.
Extract all files contained in this archive to the directory `/home/user/extracted/`.

Second, there is a voice memo located at `/app/voice_memo_001.wav`. This memo contains an important project code spoken aloud (e.g., a word followed by a number). You must transcribe this audio file to find the secret project code.

Third, after extracting the files, create a compressed tarball backup of the `/home/user/extracted/` directory. You must use an atomic write pattern: write the tarball to `/home/user/backup/.latest.tar.gz.tmp` first, and once completely written, rename it to `/home/user/backup/latest.tar.gz`. Also, generate a metadata log at `/home/user/backup/manifest.txt` listing each extracted file's path and its MD5 checksum, formatted as `MD5(filepath) = hash`.

Finally, you must write and run a Python HTTP service (using Flask, FastAPI, or the standard library) to serve the organized project data. 
The service must run on `127.0.0.1:8080`.
It must secure all endpoints by requiring an HTTP header `X-Project-Token` set exactly to the secret project code transcribed from the audio file (in ALL CAPS, stripping any punctuation).
The service must expose the following GET endpoints:
1. `/files`: Returns a JSON object with a key `files` containing a list of the extracted file paths (relative to the extracted directory).
2. `/transcript`: Returns a JSON object `{"transcript": "<the transcribed text>"}`.
3. `/backup/status`: Returns a JSON object `{"backup_path": "/home/user/backup/latest.tar.gz", "manifest_exists": true}` (or false if the manifest is missing).

Leave the HTTP server running in the background or foreground so my automated testing suite can query it.