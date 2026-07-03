Wake up. It's 3 AM and you're on-call.

PagerDuty just exploded with critical alerts from our data ingestion pipeline: the `poly-eval` service is crash-looping in production. The logs show repeated panics: `panic: runtime error: slice bounds out of range [1:25] with capacity 10`. Additionally, downstream consumers are reporting data corruption and intermittent incorrect mathematical aggregations right before the crashes occur. 

The `poly-eval` service reads a continuous binary stream of framed mathematical requests from `stdin`, evaluates polynomials concurrently for high throughput, and writes the results to `stdout`. 

Your objective is to diagnose the panics, fix any underlying concurrency bugs, handle corrupted inputs gracefully, and produce a rock-solid, fixed executable.

**System Details & Environment:**
- The main service code is located at `/app/poly-eval/`.
- The mathematical logic relies on a third-party, pre-vendored Go library located at `/app/vendor/fastmath/`. No internet access is required or permitted to fetch external packages.
- The binary stream consists of multiple sequential "frames". Each frame represents a polynomial evaluation request: `P(x) = c_0 + c_1*x + c_2*x^2 + ... + c_{N-1}*x^{N-1}`.
- Frame Format (Binary):
  - Byte 0: `N` (uint8, the number of coefficients)
  - Byte 1: `X` (int8, the variable to evaluate the polynomial at)
  - Bytes 2 to 2+N-1: `c_0` to `c_{N-1}` (int8 coefficients)

**Requirements:**
1. **Fix the Crashing:** The stream occasionally contains truncated or malformed frames where the remaining bytes are fewer than `N`. The vendor library currently panics on this edge-case data. You must intercept or fix this so that instead of panicking, the program outputs exactly `ERR_CORRUPT\n` for that specific frame, and continues processing subsequent frames.
2. **Fix the Race Conditions:** The intermittent incorrect aggregations are due to a concurrency bug (likely a race condition) during the evaluation phase when `poly-eval` processes frames in parallel. You'll need to profile or audit the code (including the vendored `fastmath` package) and fix the race.
3. **Assertion-Based Validation:** Introduce checks to ensure that the outputs are deterministic and correct. Output results must be printed as base-10 integers followed by a newline (e.g., `42\n`).
4. **Output Integrity:** Despite concurrent processing, the outputs written to `stdout` MUST maintain the exact chronological order of the input frames from `stdin`.

**Deliverable:**
When you have fixed the code, compile the final executable to:
`/home/user/poly-eval-fixed`

Our automated verifier will pipe thousands of raw fuzzed binary frames (including corrupted sequences and edge cases) into your `/home/user/poly-eval-fixed` binary and compare its `stdout` byte-for-byte against a stripped reference oracle. It must be bit-exact equivalent and complete without panicking.