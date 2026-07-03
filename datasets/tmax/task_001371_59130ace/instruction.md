We have a Rust-based telemetry processing server located in `/home/user/acoustic-node`. It analyzes acoustic sensor data to calculate precise mathematical signal variances. 

Recently, our continuous integration pipeline started failing intermittently. The calculated variance from our standard test audio file occasionally loses precision or returns incorrect aggregated values. We suspect a concurrency bug or race condition was introduced somewhere in the last 200 commits.

Your tasks are:
1. **Bisect the Repository:** The commit tagged `v1.0.0` is known to be good. `HEAD` is known to be bad. Write a script to reproduce the intermittent failure using the audio fixture located at `/app/telemetry_signal.wav`. Use `git bisect` to identify the exact commit that introduced the bug.
2. **Log the Culprit:** Write the full 40-character SHA hash of the bad commit into `/home/user/bad_commit.txt`.
3. **Fix the Bug:** Diagnose the root cause of the intermittent precision loss / race condition in the Rust source code and fix it. The calculation splits the audio processing into concurrent chunks. Ensure that the aggregation handles corrupted input frames gracefully (ignoring NaN values without poisoning the result) and maintains full `f64` precision without race conditions.
4. **Deploy the Service:** Compile and run your fixed server. It must listen on `127.0.0.1:8080`.
   - The server must expose a `POST /process` endpoint.
   - It must require an `Authorization: Bearer math-telemetry-xyz` header.
   - It should accept a JSON payload: `{"filepath": "/app/telemetry_signal.wav"}`.
   - It should return a JSON response: `{"variance": <f64_value>}`.

Leave the fixed server running in the background. An automated verifier will issue multiple HTTP requests to your server to ensure the race condition is resolved and the mathematical precision is perfectly stable.