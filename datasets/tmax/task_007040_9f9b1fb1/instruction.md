You are an open-source maintainer reviewing a broken Pull Request for a lightweight API gateway project. The project is migrating a legacy Python rate-limiting gateway to Go to improve performance, but the contributor's PR is broken.

The workspace is located at `/home/user/gateway-pr`.

Here is the situation:
1. The legacy Python implementation (`/home/user/gateway-pr/legacy_gateway.py`) correctly parsed a structured routing configuration (`/home/user/gateway-pr/routes.json`) and implemented a naive in-memory token bucket rate limiter (5 requests per second per IP).
2. The contributor attempted to translate this into Go (`/home/user/gateway-pr/main.go`). However, their Go implementation has several issues:
   - It fails to parse the nested structures in `routes.json` correctly.
   - The rate-limiting middleware is broken. It has a race condition and doesn't use Go concurrency patterns properly (they used a global map without mutexes or channels, causing panics under load).
   - It does not properly validate incoming requests against the parsed routes (requests to unknown routes should return 404, but currently return 200).
3. The contributor included a benchmarking script `/home/user/gateway-pr/bench.sh` which uses `curl` in the background to send concurrent requests.

Your task:
1. Fix the Go code in `main.go`. You must:
   - Correctly parse `routes.json`.
   - Fix the code translation: implement a thread-safe rate limiter in Go (using goroutines, channels, or `sync.Mutex`) enforcing a strict limit of 5 requests per second per IP.
   - Return HTTP 429 Too Many Requests when the limit is exceeded.
   - Return HTTP 404 Not Found for routes not defined in `routes.json`.
   - Return HTTP 200 OK with the body "Routed to [target_service]" for valid, allowed requests.
2. Build the Go server to an executable named `/home/user/gateway-pr/gateway`.
3. Run the Go server in the background on port 8080.
4. Run the benchmark script `/home/user/gateway-pr/bench.sh`.
5. Create a review summary file at `/home/user/pr_review.json` with the following exact structure:
```json
{
  "builds_successfully": true,
  "handles_concurrency": true,
  "benchmark_completed": true
}
```

Ensure the server is running and accessible on `127.0.0.1:8080` when you complete the task so the automated test suite can verify its behavior.