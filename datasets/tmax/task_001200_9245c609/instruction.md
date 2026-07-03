You are a backup administrator tasked with creating a custom archival service. We have a legacy system that requires a specific custom compression method and an authorization token left by the previous administrator in an audio memo.

Your objectives:
1. Locate and transcribe the audio file located at `/app/memo.wav`. This memo contains the secret authorization token required for the backup service.
2. Write a C++ HTTP server (using only standard libraries and basic Linux socket APIs) that listens on `127.0.0.1:8080`.
3. The server must implement two endpoints:
   - `POST /upload`
     - Requires an HTTP header: `X-Backup-Token: <token_from_audio>`
     - The request body contains raw text.
     - You must compress this text using a Custom Run-Length Encoding (RLE).
     - RLE Format: For every sequence of identical consecutive characters, output the character followed by a single byte representing the count (1 to 255). For example, "AAA" becomes `'A', 0x03`. If a character repeats more than 255 times, break it into multiple blocks.
     - Save the compressed binary data to `/home/user/archive.bin`.
     - Respond with `200 OK`.
   - `GET /download`
     - Requires the same `X-Backup-Token` header.
     - Reads `/home/user/archive.bin`, decompresses it back to the original text, and returns it as the HTTP response body with `200 OK`.

Constraints:
- You must write the server in C++ (`server.cpp`) and compile it using `g++`.
- Do not use external HTTP libraries; implement basic socket reading/parsing.
- Run the server in the background so it is active. 

Ensure the server is running and fully functional before you complete the task.