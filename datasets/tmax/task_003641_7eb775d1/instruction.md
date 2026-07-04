You are a mobile build engineer maintaining a legacy CI/CD pipeline. One of our remote automated build nodes has crashed and produced an automated diagnostic audio message. 

Your tasks are:

1. **Extract Diagnostic Info**: We have retrieved the automated voice message at `/app/alert.wav`. Transcribe it to find the dynamically assigned "fallback port" and the "secret access token" required for the fallback API.

2. **Develop the Checksum Library**: Mobile build artifacts require a fast checksum validation. Write a C function `int compute_checksum(const char* data)` that calculates and returns the bitwise XOR sum of all ASCII characters in the input string. Compile this into a shared library at `/home/user/libchecksum.so`.

3. **Build a Bash Backend Service**: 
   Create a pure Bash-driven HTTP server (using tools like `nc` or `socat` to handle networking, with a bash script as the request handler). The service must listen on `127.0.0.1` at the **fallback port** you extracted from the audio.
   It must support:
   - `GET /health`: Returns a standard HTTP `200 OK` with body `OK`.
   - `POST /process`: 
     - Must validate the `Authorization: Bearer <secret access token>` header. If invalid or missing, return `401 Unauthorized`.
     - Read the raw string from the request body.
     - Call the `compute_checksum` function from `/home/user/libchecksum.so` on the body string. You may use a short inline Python script utilizing `ctypes` within your bash handler to perform the FFI call.
     - Return a `200 OK` HTTP response where the body is the integer result of the checksum.

4. **Configure a Reverse Proxy**: 
   Set up a reverse proxy (using standard CLI tools like `socat`) listening on `127.0.0.1:9000` that transparently forwards all TCP traffic to your Bash backend service on the fallback port.

5. **Performance Benchmarking**:
   Run a benchmark sending 50 sequential requests to the `/health` endpoint through the reverse proxy at `127.0.0.1:9000`. You can use `curl` in a loop, or tools like `ab` if installed. Save the timing/output of this benchmark to `/home/user/benchmark.log`.

Leave both the backend service and the reverse proxy running in the background so they can be tested.