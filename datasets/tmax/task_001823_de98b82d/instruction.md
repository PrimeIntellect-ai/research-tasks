You are tasked with fixing and testing a broken Go backend service. 

A junior developer recently tried to organize the project files at `/home/user/app`, extracting rate limiting and validation logic into separate packages. Unfortunately, they introduced a circular dependency between the `core` and `limiter` packages, which currently prevents the project from building. They also left the rate limiter implementation incomplete and lacking tests.

Your objectives:
1. **Fix the Circular Dependency**: 
   - Identify the circular import between `app/core` and `app/limiter`.
   - Resolve it by creating a new package at `/home/user/app/models/models.go`.
   - Move the `Request` struct definition from `core` into the new `models` package.
   - Update all necessary imports across the project (`main.go`, `core/core.go`, `limiter/limiter.go`) so the project builds successfully.

2. **Implement Concurrency-Safe Rate Limiting**:
   - In `limiter/limiter.go`, implement the `Allow(req models.Request) bool` function.
   - For this simplified scenario, the limiter should be a strict, concurrency-safe counter. It must allow exactly a maximum of 5 requests in total across the lifetime of the application. 
   - Once 5 requests have been allowed, all subsequent calls to `Allow` must return `false`.
   - You must use Go concurrency primitives (e.g., `sync.Mutex` or channels) to ensure thread-safety.

3. **Write Unit Tests**:
   - Create a test file at `/home/user/app/limiter/limiter_test.go`.
   - Write a test function `TestLimiterConcurrent` that spawns exactly 10 goroutines.
   - Each goroutine should call `Allow()` simultaneously.
   - Use a `sync.WaitGroup` to wait for all goroutines to finish.
   - Assert that exactly 5 calls returned `true` and exactly 5 calls returned `false`.

4. **Compile and Verify**:
   - Compile the fixed application to a binary at `/home/user/app/server_bin` using `go build -o server_bin main.go`.
   - Run all tests in the project with verbose output and save the results to a log file: `go test ./... -v > /home/user/test_results.log`.

Ensure the final binary builds without errors and the test log file demonstrates all tests passing.