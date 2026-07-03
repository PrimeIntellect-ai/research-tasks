You are a senior support engineer investigating a catastrophic failure in a customer's embedded sensor system. The system logs events to a custom Write-Ahead Log (WAL), but a recent update corrupted the database and the device is currently in a failed state.

You need to perform a complete diagnostic and recovery process.

**Phase 1: Dependency Conflict & Regression Identification**
There is a local git repository at `/home/user/log_parser` containing the C code used to parse the customer's WAL files. 
1. The repository currently fails to build due to a dependency conflict in the `Makefile` (it is trying to link against an incompatible legacy audio library). Resolve this conflict so the project builds successfully with `make`.
2. A recent commit introduced an off-by-one boundary condition in `parser.c` that causes the parser to segfault on certain log entries. Use `git bisect` to find the exact commit that introduced the bug (you can use `make test` to check if a commit is good or bad). 
3. Fix the off-by-one error in `parser.c` on the `main` branch and rebuild the parser.

**Phase 2: Authentication & WAL Recovery**
The customer device automatically generates a spoken distress code when it enters a failure state. This audio file has been extracted to `/app/incident.wav`.
1. Transcribe the spoken codeword in `/app/incident.wav`.
2. Use the compiled `./parser` tool from `/home/user/log_parser` to recover the corrupted WAL file located at `/app/customer.wal`. You must pass the transcribed codeword as the decryption key to the parser (e.g., `./parser --key <CODEWORD> /app/customer.wal`).
3. The parser will output the recovered records. Save the exact standard output of this command to `/home/user/recovered_data.json`.

**Phase 3: Prevention & Adversarial Filter**
To prevent this corruption from happening again, we need a strict sanitization filter. 
Write a C program at `/home/user/validator.c` and compile it to `/home/user/validator`.
This program must take a single file path as a command-line argument:
`./validator <path_to_event_file>`

The event files are binary formats. A valid file strictly adheres to this structure:
- Byte 0: A magic number `0xAA`
- Byte 1: The payload length `N` (unsigned, 0 to 255)
- Bytes 2 to 2+N-1: The payload data.
- The file size MUST be exactly `N + 2` bytes. Any extra bytes or missing bytes indicate a corrupted or adversarial payload that triggers buffer overflows in legacy components.

Your validator must:
- Return exit code `0` if the file is perfectly well-formed.
- Return exit code `1` if the file is malformed, has invalid magic, or has a size mismatch (adversarial/corrupted).

The automated verifier will test your `./validator` binary against a secret corpus of clean and evil (adversarial) files.