We have a Rust-based telemetry processing server located in a Git repository at `/home/user/telemetry_svc`. Recently, we discovered a regression: the server crashes or drops data when processing payloads with slightly corrupted metadata fields (e.g., non-UTF8 bytes in the device ID). 

Previously, our legacy C-based parser handled these corrupted inputs gracefully by replacing invalid characters with a `?` character and recovering the rest of the payload. We have a stripped, legacy binary of this parser available at `/app/telemetry_oracle`. It reads a hex-encoded payload from `stdin` and outputs the parsed JSON to `stdout`.

Your tasks are:
1. **Bisect the Regression**: The current `HEAD` of the `master` branch has the bug. The commit `HEAD~200` (tagged `v1.0.0`) is known to be good. Use the oracle at `/app/telemetry_oracle` to determine the correct behavior for corrupted inputs, and bisect the repository to find the exact commit that introduced the parsing regression.
2. **Fix the Bug**: Trace the intermediate parsing state in the identified commit to understand why corrupted input handling fails. Fix the Rust server so it matches the oracle's recovery behavior exactly.
3. **Add a Regression Test**: Create a minimal reproducible example by adding a Rust unit test in `/home/user/telemetry_svc/src/main.rs` that tests the exact corrupted input that failed, ensuring it now passes.
4. **Deploy**: Start the fixed server. It must listen on `127.0.0.1:8080`. 
   - It should accept HTTP POST requests to the `/process` endpoint.
   - The body of the POST request will be raw binary telemetry data.
   - The server must respond with an HTTP 200 OK and a JSON body matching the oracle's output format.

Leave the server running in the background when you are finished.