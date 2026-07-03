You are an AI assistant helping a mobile build engineer maintain our CI/CD pipelines. We are adding a new verification step for our mobile app's audio assets (voiceovers and UI alerts) to ensure they are correctly encoded and contain the right content before packaging.

Your task is to build a REST API service that acts as our Build Artifact Audio Analyzer.

Here are the specific requirements:

1. **Shared Library FFI**:
   We have a proprietary legacy C function that calculates an audio fingerprint checksum. You must create this C file at `/app/src/fingerprint.c` with the following content:
   ```c
   #include <stdint.h>
   int compute_fingerprint(const uint8_t* pcm_data, int length) {
       int checksum = 0;
       for(int i = 0; i < length; i++) {
           checksum = (checksum + pcm_data[i]) % 99991;
       }
       return checksum;
   }
   ```
   Compile this into a shared library `/app/lib/libfingerprint.so`. Your API service must load this library and call `compute_fingerprint` via FFI (Foreign Function Interface) in your language of choice.

2. **REST API**:
   Create a web server (using Go, Python, Rust, Node, etc.) listening on `127.0.0.1:8080`.
   It must implement a `POST /analyze` endpoint.
   - The endpoint will receive a JSON payload with an authentication token and a file path: 
     `{"token": "ci-token-992", "filepath": "/app/audio/alert.wav"}`
   - If the token is not exactly `ci-token-992`, return a 401 Unauthorized status.
   - The API must handle concurrent requests efficiently.

3. **Audio Processing & Transcription**:
   When a valid request is received:
   - Extract the raw PCM data from the provided WAV file path.
   - Pass the raw bytes to the `compute_fingerprint` FFI function to get the integer checksum.
   - Use an offline transcription tool (e.g., `pocketsphinx`, `whisper`, or `ffmpeg` + a simple speech recognition library) to transcribe the spoken words in the WAV file.
   - Return a JSON response: `{"status": "success", "checksum": <int>, "transcription": "<transcribed_text>"}`.

4. **Property-based Testing**:
   Write a property-based test suite in your chosen language (e.g., using `hypothesis` in Python or `gopter` in Go) for your FFI wrapper function. The test should generate random byte arrays of varying lengths and verify that the FFI call never crashes and always returns an integer between 0 and 99990. Save this test file at `/app/tests/test_ffi`.

Please set up the environment, compile the library, write the service and tests, and start the API server in the background so it is ready to receive requests. There is a test audio file located at `/app/audio/alert.wav`.