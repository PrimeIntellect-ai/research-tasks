You are tasked with building a lightweight configuration management tracker and serving its state via a custom C-based HTTP server.

You need to complete the following multi-stage workflow:

1. **Audio Authentication Extraction:**
   There is an audio file located at `/app/auth_dictation.wav`. This file contains a spoken passcode that must be used as the API authentication token for the service you will build. Transcribe the audio (you may use available CLI tools like `ffmpeg` or `whisper` if installed, or any other method) to retrieve the token. Convert the spoken words into a single dash-separated lowercase string (e.g., if the audio says "apple banana three", the token is `apple-banana-three`).

2. **Legacy Log Parsing:**
   A legacy configuration log is located at `/app/legacy.log`. It contains multi-line records in the following format:
   ```
   [RECORD START]
   ID: <number>
   Key: <string>
   Value: <string>
   [RECORD END]
   ```
   Parse this file using shell commands or a small script. Extract all Key and Value pairs and write them to `/home/user/configs/base.conf` in the format `Key=Value` (one per line).

3. **Archive Verification & Bulk Renaming:**
   The directory `/app/updates/` contains several `.tar.gz` archives representing new configuration patches.
   - Verify the integrity of these archives (some may be corrupted).
   - Extract only the valid archives into `/home/user/configs/patches/`.
   - Recursively traverse the `patches` directory. You will find files with the extension `.conf.tmp`. Bulk rename all of these files to have the `.conf` extension instead.
   - Concatenate the contents of all the renamed `.conf` files and append them to `/home/user/configs/base.conf` to create the final configuration state at `/home/user/configs/final.conf`.

4. **C-based Configuration Server:**
   Write a C program (`/home/user/server.c`) and compile it to an executable at `/home/user/server`.
   - The server must listen for TCP connections on port `8080`.
   - It must act as a simple HTTP/1.1 server.
   - It must implement a single endpoint: `GET /api/config`.
   - The server MUST use memory-mapped I/O (`mmap`) to read `/home/user/configs/final.conf` and stream its contents in the HTTP response body.
   - The server must enforce authentication. It must check the `Authorization` header for a Bearer token matching the exact string you transcribed from the audio file (e.g., `Authorization: Bearer <token>`).
   - If the token is missing or incorrect, return a `401 Unauthorized` HTTP status.
   - If the token is correct, return a `200 OK` HTTP status with the `Content-Type: text/plain` header, followed by the memory-mapped contents of `final.conf`.

Run your C server in the background once it is compiled and ready. Do not exit the server process.

Ensure all directories (`/home/user/configs`, etc.) are created with standard user permissions.