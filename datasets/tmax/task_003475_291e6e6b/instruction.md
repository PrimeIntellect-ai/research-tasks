You are a platform engineer maintaining a CI/CD pipeline for an audio processing service. A recent commit broke the build of our legacy C-based audio metrics pipeline located in `/home/user/pipeline`. 

Your objective is to fix the build, implement a missing mock for the test suite, process a provided audio artifact, and expose the results via a C-based HTTP service.

Specifically, you need to complete the following multi-stage workflow:

1. **Fix the Build**:
   The `Makefile` in `/home/user/pipeline` currently fails with a linking error because a required module is missing from the linking stage, and there is a compilation error in `server.c`. Identify and fix the `Makefile` and C code to ensure `make all` succeeds.

2. **Implement a Test Mock**:
   The test suite requires a mock for the `telemetry_sender` interface. Write a file `/home/user/pipeline/telemetry_mock.c` that implements the `int send_telemetry(const char* event)` function. For the tests to pass, this mock must simply write the event string to `/home/user/pipeline/telemetry.log` and return 0. Integrate this into the test build.

3. **Audio Transcription**:
   Our pipeline processes voicemail drops. We have a test audio file located at `/app/voicemail.wav`. Use any available transcription tools (e.g., `whisper.cpp` or `ffmpeg` integration if present in the environment) to transcribe the spoken content of this audio file.

4. **Serve the Results**:
   The compiled C application `audio_server` must be run in the background. You must modify `server.c` to bind to exactly `127.0.0.1:9090` and act as an HTTP/1.1 server.
   It must respond to the following endpoints:
   - `GET /health` -> Returns `HTTP/1.1 200 OK\r\n\r\nOK`
   - `GET /transcript` -> Returns `HTTP/1.1 200 OK\r\n\r\n<EXACT_TRANSCRIPT>` (replace `<EXACT_TRANSCRIPT>` with the text you recovered from `/app/voicemail.wav`).
   - The server must require an Authorization header for the `/transcript` endpoint: `Authorization: Bearer ci_pipeline_token`. If missing or invalid, return a 401 Unauthorized.

Start the `audio_server` process so it listens on the specified port. The automated verifier will issue real HTTP requests to your service to confirm the task is complete.