You are a mobile build engineer maintaining a cross-platform CI/CD pipeline. You need to create a lightweight, cross-compiled Go REST API service that acts as a localized build metrics aggregator on various build nodes.

Your objective is to build this Go service in `/home/user/metrics-api` and prepare a build script for cross-compilation.

Requirements:
1. Initialize a Go module named `metrics-api` in `/home/user/metrics-api`.
2. Write a Go HTTP server that listens on port `9090`. Do not use any third-party routing frameworks (e.g., Gin or Gorilla); use only the standard `net/http` library.
3. The server must implement the following endpoints:
   - `POST /job/{platform}/{job_id}`: Parses the `{platform}` (e.g., "ios" or "android") and `{job_id}` (a string) from the URL path. It must read a JSON body with the schema `{"status": "string", "duration": int}`. It should store these metrics in memory. After successfully processing, it should call a `RecordLog` function to write to a log file, and then return a 200 OK status.
   - `GET /summary/{platform}`: Parses the `{platform}` from the URL and returns a JSON response containing the aggregated stats for that platform with the schema: `{"job_count": int, "total_duration": int}`.
4. Implement platform-specific logging using Go's conditional build tags (`//go:build`):
   - Create a file `logger_linux.go` (built only for Linux) that implements `RecordLog(platform, jobID string)`. This function must append the exact string `[LINUX] Platform: {platform}, Job: {job_id}\n` to `/home/user/metrics-api/linux_jobs.log`.
   - Create a file `logger_windows.go` (built only for Windows) that implements `RecordLog(platform, jobID string)`. This function must append the exact string `[WINDOWS] Platform: {platform}, Job: {job_id}\n` to `/home/user/metrics-api/windows_jobs.log`.
   - Ensure the main server code calls `RecordLog` appropriately without compilation errors on either OS.
5. Create a shell script at `/home/user/build_cross.sh` that cross-compiles the Go application. It must produce:
   - A Linux amd64 executable named `api-linux-amd64` in the `/home/user/metrics-api` directory.
   - A Windows amd64 executable named `api-windows-amd64.exe` in the `/home/user/metrics-api` directory.
   Ensure the script is executable.
6. Create a test script at `/home/user/test_api.sh` that does the following:
   - Starts the compiled `./api-linux-amd64` server in the background.
   - Waits 1-2 seconds for the server to start.
   - Sends a POST request to `http://localhost:9090/job/ios/101` with JSON `{"status": "passed", "duration": 120}`.
   - Sends a POST request to `http://localhost:9090/job/android/201` with JSON `{"status": "passed", "duration": 300}`.
   - Sends a POST request to `http://localhost:9090/job/ios/102` with JSON `{"status": "failed", "duration": 45}`.
   - Sends a GET request to `http://localhost:9090/summary/ios` and saves the HTTP response body to `/home/user/ios_summary.json`.
   - Kills the background API server process before exiting.
   Ensure the test script is executable.

Note: Proper synchronization (like `sync.Mutex`) should be used for the in-memory map to ensure it handles concurrent requests, even though the test script sends requests sequentially.