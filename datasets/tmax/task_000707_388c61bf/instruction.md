You are tasked with organizing a messy project directory, extracting information from an audio log, and serving the cleaned up files and metadata over a local network.

Your goals are to:
1. **Interpret Configuration**: Read `/home/user/project_rules.json`. It specifies a list of allowed extensions and a hex-encoded "magic byte" signature. 
2. **Filter & Organize**: Scan `/home/user/messy_project/`. 
   - Copy only the files that match the allowed extensions AND contain the magic byte signature anywhere in their contents (use memory-mapped I/O or streaming to efficiently check the files).
   - Place the filtered files into `/home/user/clean_project/`.
3. **Audio Extraction**: There is an audio file located at `/app/voice_memo.wav`. You must transcribe the spoken English content in this file (you may install and use lightweight tools like `openai-whisper` or `SpeechRecognition` to do this). Let the transcribed text be `TRANSCRIPT`.
4. **Archive**: Create an uncompressed tar archive named `/home/user/clean_backup.tar` containing the contents of `/home/user/clean_project/`.
5. **Serve the Data (Multi-Protocol)**:
   Write and start a Python script that runs two network services concurrently:
   - **Service 1 (HTTP)**: Listen on `127.0.0.1:8080`. Serve the `/home/user/clean_backup.tar` file when a GET request is made to `/backup.tar`.
   - **Service 2 (TCP)**: Listen on `127.0.0.1:9090`. When a client connects and sends the exact `TRANSCRIPT` string (case-insensitive, ignoring leading/trailing whitespace and punctuation), the server must reply with the exact SHA-256 hash of `/home/user/clean_backup.tar`, followed by a newline `\n`, and then close the connection. If the wrong string is sent, reply with `DENIED\n` and close the connection.

Ensure the server process remains running in the background or foreground so that it can be verified. Do not use external web frameworks like Django; standard library or lightweight frameworks like Flask/socketserver are preferred.

Note: The messy project files and configuration will be generated for you when the environment starts.