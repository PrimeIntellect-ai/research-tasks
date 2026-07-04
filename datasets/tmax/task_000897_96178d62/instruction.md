I need your help debugging and fixing a regression in our custom telemetry ingestion server. We recently merged a large set of updates, and now our server is crashing or dropping data when handling legacy binary payloads from some of our older IoT devices. 

Here is the situation:
1. **The Codebase:** The source code for the server is located in `/home/user/telemetry_server/`. It's a C-based service that handles both a custom TCP binary protocol for data ingestion and an HTTP endpoint for health checks.
2. **The Regression:** Somewhere in the last 200 commits, a bug was introduced that causes the server to improperly parse UTF-8 encoded sensor names when they are slightly malformed (corrupted input handling/encoding issue). Instead of sanitizing the input or dropping the specific malformed packet gracefully, the server now corrupts its internal state or segfaults, breaking dependency communication with our downstream database mock.
3. **The Reference Oracle:** We have an older, stripped binary of the server that perfectly handles these legacy payloads. It is located at `/app/telemetry_oracle`. You can use it to understand the expected behavior (e.g., how it responds to specific byte sequences). 
4. **Your Goal:**
   - Use `git bisect` to identify the exact commit that introduced the regression. 
   - Analyze the buggy C code in the commit and fix the serialization/encoding logic so that it properly recovers from corrupted sensor name strings (it should replace invalid UTF-8 bytes with the `?` character and continue parsing, exactly like the oracle does).
   - Compile your fixed version.
   - Start the fixed service. It must listen on `127.0.0.1:8080` for HTTP GET health checks (returning `{"status": "ok"}` on `/health`) and on `127.0.0.1:9090` for the custom TCP telemetry protocol.
   - The TCP protocol expects a simple 16-byte authentication token (`AUTH_TOKEN: 8a9b4c2d-1234`) as the first line before accepting binary telemetry frames.

Please leave the fixed server running in the background. Write the Git SHA of the commit that introduced the bug into `/home/user/bad_commit.txt`.