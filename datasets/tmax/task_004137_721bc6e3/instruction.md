I am in the process of migrating a legacy audio processing pipeline. The old system was written in Python 2 and relied on a custom C++ shared library built via CMake. During our migration to a more lightweight microservice architecture, we decided to drop Python completely for the API layer and use a Bash-based HTTP server, while retaining the C++ core utility.

However, I'm running into several issues:
1. **CMake Linking Error:** The C++ project is located in `/home/user/legacy_audio`. When I build it, it creates a shared library `libaudio_hash.so` and an executable `hasher_cli`. However, running `./build/hasher_cli` fails because it can't find the shared library at runtime. I don't want to rely on `LD_LIBRARY_PATH`. Please fix the `CMakeLists.txt` so that the executable can find the shared library using a proper RPATH configuration (relative to the executable's location).
2. **Audio Transcription:** There is a legacy voicemail file located at `/app/voicemail.wav`. We need to recover a secret seed phrase spoken in this audio. Use whatever tools you have available to transcribe it.
3. **Bash HTTP API:** Write a Bash-based HTTP server that listens on `127.0.0.1:9090`. You can use `socat` or `nc` to handle the socket bindings. 
   - The server must accept `POST /hash` requests containing a JSON payload with a `transcript` field.
   - It should parse the JSON to extract the transcript.
   - It must run the fixed `hasher_cli` tool, passing the transcribed text from the JSON and the "secret seed phrase" you recovered from `/app/voicemail.wav` as command-line arguments.
   - It must return a valid HTTP 200 response with a JSON payload: `{"status": "success", "hash": "<output_from_cli>"}`.
   - If the JSON is malformed, return HTTP 400.
4. **Property-Based Testing:** Create a script at `/home/user/fuzz_test.sh` that generates 50 random valid and invalid JSON payloads, sends them to `127.0.0.1:9090/hash` via `curl`, and verifies that the server never drops the connection unexpectedly and always returns either HTTP 200 (with valid JSON) or HTTP 400.

Please bring up the HTTP server in the background once completed. The automated test will send requests to `127.0.0.1:9090` to verify your implementation.