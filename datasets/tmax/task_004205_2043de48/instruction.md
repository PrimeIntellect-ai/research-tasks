You are helping me migrate a legacy Python 2 audio processing service to a modern C++ gRPC backend. The legacy system used custom HTTP-like string payloads for routing requests to audio transcription and processing pipelines. Over time, the routing logic accumulated a lot of technical debt and became vulnerable to circular routing loops and malformed payload injection.

I need you to implement the new C++ backend with the following requirements:

1. **gRPC Service Design**:
   Create a protobuf definition (`/home/user/workspace/audio_router.proto`) defining a service `AudioRouter` with an RPC `ProcessRequest`. The request message should contain a string `route_path` and a string `audio_identifier`. The response should contain a boolean `accepted` and a string `result`.

2. **Custom URL Routing & Parameter Parsing**:
   Implement a custom C++ routing tree (e.g., a Radix tree or optimized prefix tree) in `/home/user/workspace/router.h` and `router.cpp` that parses the `route_path`.
   Valid routes must follow the pattern: `/v3/api/audio/{action}/{format}`.
   - `{action}` can only be `transcribe`, `analyze`, or `metadata`.
   - `{format}` can only be `wav`, `mp3`, or `flac`.
   - Any query parameters appended (e.g., `?lang=en&model=fast`) must be correctly parsed into a key-value map.
   - The router MUST strictly reject paths containing directory traversal (`../`), null bytes (`%00`), or unknown actions/formats. 

3. **Audio Fixture Processing**:
   When a valid `transcribe` request for a `wav` file is received, the service should read the audio file specified by `audio_identifier`. We have a sample audio file located at `/app/audio_fixture.wav`. Your service should execute a simple command-line transcription tool (assume `whisper.cpp` is available in `/usr/local/bin/whisper` and outputs text) on this file and return the transcript in the `result` field. For other valid requests, just return `result: "ok"`.

4. **Adversarial Corpus Verification**:
   I have provided two sets of route requests in `/home/user/workspace/test_corpora/`:
   - `clean_routes.txt`: A list of valid route paths.
   - `evil_routes.txt`: A list of malformed, malicious, or cyclic route paths.
   
   Write a C++ test binary (`/home/user/workspace/verify_router`) that loads both files. It should instantiate your custom routing structure, feed it every line from `clean_routes.txt` (which must all be accepted) and `evil_routes.txt` (which must all be rejected). It should print exactly:
   `CLEAN_PASSED: <count>`
   `EVIL_REJECTED: <count>`

Write a `Makefile` to compile the protobufs, the gRPC server (`/home/user/workspace/server`), and the `verify_router` binary. Start the server on port `50051`. Then run your `verify_router` binary and write its output to `/home/user/workspace/router_verification.log`.