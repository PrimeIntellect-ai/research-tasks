You are acting as a compliance analyst for a financial institution. Part of our daily audit trail generation relies on a legacy proprietary tool that generates cryptographic compliance tokens based on file integrity hashes and network policy configurations. 

Unfortunately, we have lost the source code for this token generator. We only have the stripped, compiled Linux binary located at `/app/audit_oracle`. 

We need to modernize our stack. Your task is to reverse-engineer the behavior of this binary and write a clean, bit-exact equivalent implementation in Go.

**Requirements:**
1. Analyze the `/app/audit_oracle` binary. It accepts exactly one command-line argument: a string representing an audit event.
2. The input string format is exactly `[8-char hex file hash]:[network port]:[10-digit unix timestamp]` (e.g., `a1b2c3d4:8080:1690000000`).
3. Write a Go program at `/home/user/token_gen.go` that implements the exact same logic.
4. Your Go program must accept the same command-line argument and print *only* the resulting token to standard output, matching the Oracle's output exactly (including any trailing newlines if present, though standard `fmt.Println` or equivalent matching is expected).
5. Compile your program to an executable located at `/home/user/token_gen`. 

Our automated CI pipeline will test your compiled binary against the legacy `/app/audit_oracle` by fuzzing both with thousands of random compliance audit strings and asserting that the outputs are strictly identical.