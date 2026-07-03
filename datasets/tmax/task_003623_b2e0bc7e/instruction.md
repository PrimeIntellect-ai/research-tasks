You are tasked with fixing and completing a Go-based audio processing microservice located in `/home/user/audio-svc`. The service uses a C library via `cgo` to extract embedded transcript metadata from WAV files. Currently, the project fails to compile and crashes at runtime due to memory safety issues in the C code, and the HTTP API is incomplete.

Here are your objectives:

1. **Fix Memory Safety and Compilation:**
   The C library (`parser/libaudio.c` and `parser/libaudio.h`) contains undefined behavior and memory leaks when parsing the custom text chunks in WAV files. Fix the C code so it correctly reads the text payload without buffer overflows or segmentations faults. The Go wrapper `parser/parser.go` should compile successfully alongside it.

2. **Semantic Versioning and API Implementation:**
   Implement the HTTP POST endpoint `/api/v1/extract` in `main.go`. 
   The endpoint must check the `X-App-Version` header. You must implement semantic version comparison. If the version provided is strictly less than `2.1.0-beta`, return an HTTP 426 (Upgrade Required).

3. **Audio Fixture Processing & Serialization:**
   When a valid request is received, the service must use the fixed C library to parse the audio file located exactly at `/app/transmission.wav`.
   The C library extracts raw metadata in an old schema format. You must perform a schema migration in memory and serialize the response as JSON. 
   Old schema from C: `{"req_id": <int>, "raw_text": "<string>", "timestamp": <int>}`
   New JSON schema required by API: `{"transmission_id": <int>, "transcript": "<string>", "migrated": true}`

4. **Service Execution:**
   The Go HTTP server must listen continuously on `127.0.0.1:8080`. Ensure the service is running in the background or foreground when you finish your task. Do not require authentication tokens.

All necessary files (except `/app/transmission.wav` which is already provided) are in `/home/user/audio-svc`. Make your edits, compile, and start the service.