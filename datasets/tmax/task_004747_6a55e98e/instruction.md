You are an operations engineer triaging an incident. The automated build and test pipeline for a legacy data processing service has started failing. 

The service relies on a compiled binary utility located at `/home/user/app/bin/parser` that reads a custom binary log file and outputs JSON. Recently, upstream log generators changed their output format, causing the parser to output truncated or garbled JSON. The pipeline's automated test step now fails because the parsed output no longer matches the expected data.

Your goal is to diagnose the failure, fix the input data, and restore the build:

1. Navigate to `/home/user/app/` and run `make test`. You will observe a failure because the output of the parser processing `/home/user/app/data/raw.dat` does not match `/home/user/app/expected.json`.
2. You do not have the source code for the `parser` binary. You must reverse engineer its behavior or analyze its execution against `raw.dat` to determine how the custom binary format is structured (e.g., headers, lengths, string encodings).
3. Identify the encoding issue in `raw.dat` that is causing the parser to read the string payload incorrectly.
4. Write a script to convert the malformed `/home/user/app/data/raw.dat` into a corrected file at `/home/user/app/data/fixed.dat`. The corrected file must have the same custom binary format structure (matching the magic header and appropriate length indicators) but with the string payload encoded correctly so the binary parser outputs the expected JSON.
5. Update the `Makefile` to use `data/fixed.dat` instead of `data/raw.dat` for the test target so that `make test` passes successfully.
6. Create a log file at `/home/user/app/resolution.json` summarizing your findings. It must contain valid JSON with exactly two keys:
   - `"magic_hex"`: The 4-byte magic header value expected by the binary at the start of the file, formatted as a lowercase hex string without the "0x" prefix (e.g., "aabbccdd").
   - `"original_encoding"`: A string indicating the problematic character encoding that was used for the text payload in the original `raw.dat` file (e.g., "utf-16le").

Your task is complete when `make test` succeeds and `resolution.json` contains the correct values.