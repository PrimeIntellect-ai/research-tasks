You are an open-source maintainer reviewing a broken Pull Request for a lightweight API Gateway written in C. The contributor attempted to add a custom URL-decoding module to sanitize incoming request paths (mitigating directory traversal and encoding attacks), but the PR fails under concurrent stress tests and lacks cross-compilation support.

Your task is to fix the PR, improve the test suite, and build the release binaries.

**Step 1: Fix the C Character Encoding Bug**
The file `/home/user/gateway/urldecode.c` contains a function `char* decode_url(const char *input)`. The contributor's implementation miscalculates the required buffer size and fails to properly decode hex sequences (like `%20`), resulting in heap corruption. 
- Fix `urldecode.c` so it correctly decodes standard percent-encoded strings. 
- Ensure it handles invalid encodings (e.g., a `%` followed by non-hex characters or end-of-string) by leaving them as-is.
- Prevent any buffer overflows or memory leaks.

**Step 2: Upgrade the Go Stress Test using Concurrency**
The test suite at `/home/user/gateway/tests/stress.go` currently executes the compiled C binary 10 times sequentially. 
- Modify `stress.go` to use Go concurrency patterns (goroutines and channels, or `sync.WaitGroup`).
- It must execute the binary 100 times concurrently with various encoded payloads to ensure the C program doesn't crash under parallel execution (simulating high traffic).
- The Go script should print "PASS" to stdout only if all 100 executions return a 0 exit code.

**Step 3: Cross-Compilation and Conditional Builds**
The gateway needs to be built for both x86_64 and ARM64 platforms, with a specific security macro enabled.
- Create a directory `/home/user/build/`.
- Compile the gateway (`/home/user/gateway/main.c` which includes `urldecode.c`) for **Linux x86_64** (using standard `gcc`) and output to `/home/user/build/gateway_amd64`.
- Compile the gateway for **Linux ARM64** (using `aarch64-linux-gnu-gcc`) and output to `/home/user/build/gateway_arm64`.
- **Crucial:** Both builds must be compiled with the `-DSECURE_MODE` flag. (The `main.c` file has conditional logic that changes behavior if this is set).

**Step 4: Verification Logging**
Once everything is fixed, compiled, and tested:
1. Run your updated Go stress test.
2. Generate the SHA256 hashes of the two compiled binaries.
3. Save these hashes into `/home/user/build/hashes.txt` in the format:
```
<sha256>  gateway_amd64
<sha256>  gateway_arm64
```