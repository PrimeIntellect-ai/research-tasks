You are tasked with debugging and fixing a regression in a Rust-based system daemon. 

The source code is located in a git repository at `/app/system-daemon`. The `main` branch currently fails when handling certain requests. Specifically, when the server receives an HTTP `GET /api/v1/metrics` request, the server process crashes with a segmentation fault (core dump) or panic.

The last known good version is tagged `v1.0.0`, which is exactly 200 commits behind `main`.

Your objectives are:
1. **Bisect the regression**: Identify the exact commit hash that introduced the crash. Write this full commit hash to a file named `/home/user/bad_commit.txt`.
2. **Analyze the crash**: Investigate the stack trace or intermediate state to understand why the server crashes on `main` when handling the metrics endpoint. 
3. **Fix the bug**: Modify the source code on the `main` branch to resolve the crash. The server must successfully build and run without compiler or linker errors.
4. **Deploy the server**: Start the fixed server in the background so that it listens on `0.0.0.0:8080`.

**Server Specifications**:
- The server must listen on `0.0.0.0:8080`.
- It must respond to HTTP `GET /api/v1/metrics` with an HTTP 200 OK and the exact body `Metrics OK`.
- Any authentication headers or other endpoints can be ignored.

Please leave the server running in the background listening on port 8080 once you have fixed the code and verified it works.