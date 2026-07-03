I am a QA engineer setting up a test environment for a new Web Application Firewall (WAF) payload serialization component. The developer provided a fast C-based hex-encoder, but the source code and build files are broken.

Your task is to fix the C program, compile it, and create a Bash-based test harness that generates test data, serializes it, runs the encoder, verifies the output, and benchmarks its performance.

**Step 1: Fix and Compile the C Program**
In `/home/user/waf_encoder/`, you will find `encoder.c` and a `Makefile`.
1. `encoder.c` expects to read a serialized payload from standard input in the format `SIZE:DATA` (e.g., `3:ABC`), and outputs the hex-encoded version of `DATA` to standard output. However, it fails to compile due to missing headers and strict compiler flags. Fix `encoder.c` so it compiles without warnings.
2. The `Makefile` is broken (likely due to incorrect indentation/spaces). Fix it.
3. Run `make` to produce the `./encoder` binary in `/home/user/waf_encoder/`.

**Step 2: Create the Test Harness**
Write a Bash script at `/home/user/test_harness.sh` that performs the following steps when executed:
1. Generates a raw payload file at `/home/user/payload.dat` containing exactly 100,000 uppercase `X` characters (no newlines).
2. Creates a serialized payload file at `/home/user/payload.ser` following the format `SIZE:DATA` (where `SIZE` is the exact byte count of the payload, so `100000:XXXX...`).
3. Captures the start time in milliseconds.
4. Feeds `/home/user/payload.ser` via standard input to `/home/user/waf_encoder/encoder`, saving the output to `/home/user/payload.enc`.
5. Captures the end time in milliseconds and calculates the duration (`end - start`).
6. Verifies the output by using standard Bash utilities (like `xxd` or `od`) to hex-encode `/home/user/payload.dat`. If `/home/user/payload.enc` exactly matches the expected hex representation (lowercase, no spaces, no newlines), record a pass.
7. Appends the results to `/home/user/qa_log.txt` in exactly this format:
   ```
   TEST: WAF_ENCODER
   STATUS: PASS
   TIME_MS: [Calculated Duration]
   ```
   *(If the output does not match, output `STATUS: FAIL` instead).*

Ensure the script `/home/user/test_harness.sh` is executable and run it so the final system state contains the compiled binary, all generated payload files, and the `qa_log.txt` file. You may only use standard coreutils, built-ins, and standard CLI tools for your bash script.