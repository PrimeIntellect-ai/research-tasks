You are a security researcher analyzing a suspicious crash in a custom protocol parsing microservice. The service recently crashed, and you need to investigate the root cause, identify the specific input that triggered the crash, and patch the vulnerability.

You have been provided with the following files:
- The parser source code: `/home/user/parser/` (a Cargo project)
- Three log files from different microservices that route traffic to the parser:
  - `/home/user/logs/auth.log`
  - `/home/user/logs/router.log`
  - `/home/user/logs/parser.log`

The crash was caused by a buffer overflow / out-of-bounds memory access originating from a vulnerable length-calculation formula within the `extract_payload` function in `/home/user/parser/src/main.rs`. 

Your tasks are:
1. **Log Timeline Reconstruction:** Analyze the three log files to reconstruct the sequence of events. Identify the specific Transaction ID (e.g., `TXN-XXXX`) that caused the parser to crash. The parser crashes immediately upon processing this malformed transaction, so it won't have a completion log entry.
2. **Identify and Log the Crashing Input:** Write ONLY the crashing Transaction ID into a new file at `/home/user/crash_tx.txt`.
3. **Correct the Implementation:** Inspect `/home/user/parser/src/main.rs`. The `extract_payload` function uses an `unsafe` block to slice the packet based on a calculated `header_len`. Fix the formula and bounding logic so that if the calculated `header_len` is strictly greater than the length of the `packet`, the function gracefully returns an empty slice (`&[]`) instead of underflowing/overflowing.
4. **Verify the Fix:** Ensure your modified code compiles successfully by running `cargo build` inside the `/home/user/parser/` directory.

Do not change the function signature of `extract_payload`. Only fix the internal logic to prevent the out-of-bounds access.