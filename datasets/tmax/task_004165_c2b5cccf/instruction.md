You are an integration developer responsible for building a lightweight testing API that analyzes video frames. 

We have a buggy C application located at `/home/user/analyzer/frame_analyzer.c`. It is designed to read a raw 24-bit RGB frame (854x480 resolution) and compute a simple checksum (the sum of all byte values modulo 256). Currently, it crashes due to a memory allocation bug and undefined behavior.

Additionally, we have a test video located at `/app/drone_footage.mp4`.

Your tasks are:
1. Fix the memory bugs in `/home/user/analyzer/frame_analyzer.c` and update its `/home/user/analyzer/Makefile` so it compiles cleanly without warnings into an executable named `frame_analyzer`.
2. Write a Bash-based HTTP server script at `/home/user/api_server.sh` that listens on `127.0.0.1:9090`. 
3. The Bash API must implement the following REST endpoint:
   - `GET /api/v1/analyze?time=<seconds>`
   - It must require an `Authorization: Bearer test-api-key-88` header. Return `401 Unauthorized` if missing or incorrect.
   - When a valid request is received, it should use `ffmpeg` to extract exactly one frame from `/app/drone_footage.mp4` at the specified `<seconds>` (e.g., `00:00:05`) as a raw 854x480 RGB24 image.
   - It must pass this raw image file to the compiled `frame_analyzer`.
   - It must return an HTTP 200 response with `Content-Type: application/json` and the body: `{"time": "<seconds>", "checksum": <result>}`.
4. Start the server in the background so it is ready to accept requests.

Ensure your API server script correctly parses the URL routing parameters and HTTP headers from incoming TCP connections (you may use `nc` or `socat` within your bash script). Do not use external web frameworks like Python's Flask or Node.js; the server must be implemented primarily in Bash.