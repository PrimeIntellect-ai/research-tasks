You are a platform engineer maintaining the CI/CD pipeline for an API Gateway written in Go. The gateway uses conditional builds to switch between a highly optimized, hardware-specific rate limiter (`fast`) and a concurrency-based fallback rate limiter (`fallback`).

The CI pipeline is currently failing on the `fallback` variant build and test stages. Your task is to fix the application code, update the test fixtures, and successfully cross-compile the binaries for our deployment targets.

The project is located at `/home/user/gateway`.

**Objectives:**

1. **Fix the Goroutine Leak:**
   Run `go test -tags=fallback .` in the `/home/user/gateway` directory. The test `TestLimiter_Concurrency` will fail due to a goroutine leak. The leak is caused by a blocked channel inside the `Allow()` method of `limiter_fallback.go` when the request context times out or is cancelled. Analyze the concurrency pattern and fix the channel synchronization so goroutines are not leaked.

2. **Complete the Test Fixture:**
   In `limiter_test.go`, the test `TestLimiter_Validation` is failing. It expects the request to have a specific header to pass validation. Update the mock request fixture in `TestLimiter_Validation` to include the header `X-App-Config` with the value `valid-config` so the test passes.

3. **Cross-Compilation:**
   Once all tests pass, manually cross-compile the gateway binaries. Output them to the `/home/user/gateway/build/` directory (you will need to create this directory).
   - Build 1: Target Linux `amd64`, use build tag `fast`, and name the binary `gateway_fast_amd64`.
   - Build 2: Target Linux `arm64`, use build tag `fallback`, and name the binary `gateway_fallback_arm64`.

Your task is complete when both binaries exist in the `build/` directory with the correct architectures and all tests pass cleanly for both tags without leaking goroutines.