You are tasked with fixing a failing build for a Rust project and recovering a lost configuration key from a corrupted fuzzer crash dump.

A previous fuzzer run crashed and produced a memory dump file located at `/home/user/project/fuzz_crash.bin`. The project's build script (`/home/user/project/build.rs`) attempts to read this file to extract the application's secret key and embed it into the compiled binary. However, because the crash dump contains raw, corrupted binary data (invalid UTF-8), the build script panics and the build fails.

Your objectives are:
1. Diagnose the build failure in `/home/user/project`.
2. Extract the secret key from the binary crash dump (`/home/user/project/fuzz_crash.bin`). The key is prefixed with `APP_SECRET_KEY=` and is exactly 32 hexadecimal characters long.
3. Save *only* the 32-character hexadecimal key (no prefix, no newlines) into a file at `/home/user/recovered_key.txt`.
4. Fix the build failure. If you inspect `/home/user/project/build.rs`, you will notice it has a fallback mechanism: it will skip reading the corrupted binary file if a specific environment variable is set. Use this mechanism or modify `build.rs` so that `cargo build` completes successfully. 

Ensure that `cargo build` inside `/home/user/project` compiles without errors before you finish.