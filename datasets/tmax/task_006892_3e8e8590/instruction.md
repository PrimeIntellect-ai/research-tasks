You are a security researcher analyzing a suspicious binary dropping network payloads. 

You have been provided with:
1. `/home/user/generator`: An obfuscated ELF binary dropped by malware that generates network payloads.
2. `/home/user/parser`: A Go project containing an initial implementation of a parser (`parser.go`) meant to decode these payloads.

Your analysis has revealed that the Go parser crashes intermittently in production when processing traffic, and sometimes panics outright on malformed data.

Your objectives are:
1. **Reverse Engineer the Magic Header:** Analyze the `/home/user/generator` binary (e.g., using `strings`, `ltrace`, or `objdump`) to discover the 4-byte magic string it prepends to all payloads. Save this exact 4-byte string to `/home/user/magic.txt`.
2. **Format Parsing Edge-Case Repair:** The `ParsePayload(data []byte)` function in `/home/user/parser/parser.go` panics if the payload specifies a length byte that extends beyond the actual buffer size. Modify `ParsePayload` so that it safely returns `errors.New("invalid length")` instead of panicking.
3. **Concurrency Bug Fix:** The `ProcessConcurrent(payloads [][]byte)` function suffers from a race condition (intermittent failure) because it writes to a shared map `ParsedResults` from multiple goroutines without synchronization. Fix the race condition in `parser.go` using a `sync.Mutex`.
4. **Regression Test Construction:** Create `/home/user/parser/parser_test.go` and write a test function named `TestParserRegression(t *testing.T)` that verifies both of your fixes. The test must:
   - Call `ParsePayload` with a synthetically crafted payload (using the magic header you discovered) that triggers the out-of-bounds edge case, and assert that it returns the expected error instead of panicking.
   - Call `ProcessConcurrent` with at least 10 concurrent valid payloads to ensure the race condition is resolved (it must pass `go test -race`).

Ensure your test passes successfully. Do not change the function signatures of `ParsePayload` or `ProcessConcurrent`.