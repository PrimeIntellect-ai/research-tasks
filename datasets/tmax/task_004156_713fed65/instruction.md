Hello! I am an open-source maintainer reviewing a broken PR for our security team's internal web tool. The PR attempts to port our legacy C server to Rust, but it is incomplete, fails to build, and doesn't meet our deployment targets. 

The starter codebase is located at `/home/user/audio-server` (you will need to initialize a basic Cargo project there if it's missing or broken).

Your task is to fix the PR and ensure the system meets the following specifications:

1. **HTTP Server**: Implement a Rust web server that binds and listens on `127.0.0.1:9000`.
2. **Audio Processing**: The server must implement a `GET /analyze` endpoint. When this endpoint is requested, the server must read the audio file located at `/app/voicemail.wav`, transcribe its spoken English content, and return a JSON response: `{"secret": "<transcribed_text>"}`. 
   - *Hint*: You may install and use external CLI tools (like `whisper.cpp`, `ffmpeg`, etc.) to perform the transcription and execute them from within your Rust server.
3. **Constraint Satisfaction**: Our legacy C tool had a security constraint: it rejected any audio that did not contain the keyword "code". Implement this constraint in your Rust server. If the transcribed text does not contain the word "code" (case-insensitive), the endpoint must return an HTTP 400 status code with the JSON body `{"error": "constraint failed"}`.
4. **Cross-Compilation**: We deploy this in a minimal Alpine container. You must compile the final server as a statically linked release binary for the `x86_64-unknown-linux-musl` target. Place the compiled binary at the exact path: `/home/user/release_bin`.
5. **Execution**: Once compiled, start your server in the background so that it is actively listening on `127.0.0.1:9000` when you complete your task.

Please ensure the server runs robustly and handles the transcription and HTTP protocol correctly.