You are a platform engineer maintaining a CI/CD pipeline for a high-performance web API gateway. The gateway is written in Go to handle high concurrency, but it offloads a critical security function (HTML tag stripping) to a highly optimized C++ library via FFI (cgo). 

Recently, the security regression suite in the CI pipeline has been failing randomly with segmentation faults. The test suite uses Go concurrency patterns (spinning up multiple goroutines) and property-based testing principles to fuzz the C++ FFI layer with varied, concurrent inputs.

Your investigation has isolated the issue to the C++ code at `/home/user/api-gateway/sanitizer.cpp`. There is a memory safety issue (undefined behavior) in how the buffer is allocated and null-terminated.

Your tasks are:
1. Identify and fix the memory safety bug in `/home/user/api-gateway/sanitizer.cpp`. 
2. Verify your fix by running the Go tests. You can run `go test` in the `/home/user/api-gateway` directory.
3. Once the tests pass without crashing, run the performance benchmark using `go test -bench . > /home/user/api-gateway/bench_results.txt`.

The CI pipeline expects the benchmark results to be strictly saved to `/home/user/api-gateway/bench_results.txt`. Do not modify the Go test file (`/home/user/api-gateway/sanitizer_test.go`).