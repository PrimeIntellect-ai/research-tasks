You are tasked with fixing and deploying a mathematical Go service that has recently suffered a severe regression. 

Your workflow involves several steps:

1. **Audio Artefact Extraction:**
   There is an audio file located at `/app/voicemail.wav`. It contains a spoken message from the original developer stating a 5-digit authorization PIN required to use the API. You must transcribe this audio to recover the PIN.

2. **Git Regression Bisection & Code Fixing:**
   Navigate to the Git repository at `/home/user/math_server`. This repository contains the source code for a Go-based mathematical API. 
   Currently, the `main` branch fails to compile due to a linker/compiler error introduced in the very last commit. 
   First, diagnose and fix the compilation error in `main.go`.
   Once it compiles, you will notice that the API produces incorrect results or intermittently fails when processing concurrent requests to its mathematical endpoints. 
   A regression was introduced somewhere in the last 200 commits. The commit exactly 200 commits ago (which is tagged as `v1.0.0`) is known to be mathematically correct and bug-free. 
   Use `git bisect` (and write a small test script if necessary) to isolate the exact commit that introduced the mathematical/concurrency bug. Revert or fix the logic from that specific bad commit so that the service functions correctly and safely handles concurrent requests.

3. **Service Deployment:**
   Update the HTTP server in `main.go` so that the `/prime_factors` endpoint (which accepts a POST request with JSON `{"number": <int>}` and returns `{"factors": [<int>, ...]}`) requires an `Authorization: Bearer <PIN>` header, using the 5-digit PIN you extracted from the audio.
   Build and start the Go server so that it continuously listens on `127.0.0.1:9000`.

Leave the server running in the background. Do not stop it. An automated verifier will issue concurrent HTTP POST requests to `http://127.0.0.1:9000/prime_factors` using the recovered authorization PIN to ensure the mathematical regression is resolved and no race conditions occur.