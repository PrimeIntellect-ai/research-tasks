You are a backend web developer building a high-performance data ingestion service for a real-time web dashboard. The service receives WebSocket messages containing telemetry data. The Nginx reverse proxy strips the WebSocket framing and pipes the raw text payloads directly into your program's standard input, line by line.

Your task is to implement this processor in C, focusing on strict validation, state machine parsing, and rate limiting, and then to write a property-based test in Python to ensure your parser is memory-safe.

Step 1: Write the Processor in C
Create a file at `/home/user/telemetry.c` and compile it to an executable at `/home/user/telemetry` (using `gcc -O2 telemetry.c -o telemetry`).
The program must read lines from `stdin` until EOF. Each line represents one WebSocket text payload.
The strict expected format for each line is: `DEVICE=<ID>;DATA=<VAL>\n`
- `<ID>` must be exactly 4 uppercase hexadecimal characters (`0-9`, `A-F`).
- `<VAL>` must be a positive integer (1 or more base-10 digits).
- No spaces or other characters are allowed anywhere in the line.
- You must parse this using a custom character-by-character state machine (do not just use `sscanf` or regex).

Validation & Rate Limiting:
- Keep an in-memory tally of valid messages received per `<ID>`.
- The maximum allowed messages per device is 2. 
- For each line read, your program must output exactly one line to `stdout`:
  - If the format is invalid in any way, output: `ERROR`
  - If the format is valid and the device has sent <= 2 messages, output: `OK <ID> <VAL>`
  - If the format is valid but the device has already sent 2 valid messages, output: `LIMIT <ID>`

Step 2: Property-Based Testing
To ensure your C state machine doesn't segfault on malformed WebSocket payloads, write a Python script at `/home/user/prop_test.py` that uses the `hypothesis` library.
The script should:
1. Generate random binary or text strings using `hypothesis.strategies`.
2. Feed them to `/home/user/telemetry` via `subprocess`.
3. Assert that the C program exits with a return code of `0` (no crashes/segfaults) and that the number of output lines exactly matches the number of input lines.
(You don't need to run the test script to complete the task, but the file must exist and be valid).

Step 3: Execution
We have placed a test file at `/home/user/ws_stream.txt`. Run your compiled `/home/user/telemetry` binary using this file as standard input, and redirect the output to `/home/user/results.log`.

Make sure `/home/user/results.log` is strictly formatted as described.