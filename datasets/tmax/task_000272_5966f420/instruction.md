You are a platform engineer maintaining a CI/CD pipeline. Your team recently introduced a voice-based deployment instruction system. 

We have received a voice memo for a new pipeline configuration located at `/app/pipeline_instruction.wav`.

Your task is to implement a Python WebSocket server that acts as a remote build worker based on the instructions in the audio.

Requirements:
1. **Audio Parsing**: Extract the target CPU architecture and the secret authentication token from the audio file `/app/pipeline_instruction.wav`.
2. **WebSocket Server**: Create a Python WebSocket server (using the `websockets` library or `asyncio`) listening on `127.0.0.1:8081`. The server must remain running in the background.
3. **Protocol**:
   - The server will receive a JSON payload with the schema: `{"token": "<auth_token>", "c_code": "<raw_c_source_code>"}`.
   - If the `token` does not exactly match the secret token spoken in the audio file, the server must close the connection with WebSocket close code `1008` (Policy Violation).
   - If the token matches, the server must process the `c_code`.
4. **Cross-Compilation & Assembly Analysis**:
   - Write the `c_code` to a temporary file.
   - Use the appropriate cross-compiler for the architecture mentioned in the audio (e.g., if it's `aarch64`, use `aarch64-linux-gnu-gcc`) to compile the C code to assembly only (using the `-S` flag) with `-O0` optimization.
   - Parse the generated assembly file and count the exact number of lines that contain the `mov` instruction mnemonic (case-insensitive, looking for the `mov` instruction itself, e.g., `mov`, `mov w0, w1`). Ignore lines where `mov` is just part of a word or filename, but match the instruction.
5. **Response**:
   - Send a JSON response back over the WebSocket: `{"result": "compiled", "mov_count": <integer>}`.
   - Keep the server running to accept subsequent connections.

Make sure you install any necessary system packages for cross-compilation and audio transcription (e.g., `ffmpeg`, `aarch64-linux-gnu-gcc`, Whisper, etc.).
Leave the server running in the background so the automated verification suite can connect to it.