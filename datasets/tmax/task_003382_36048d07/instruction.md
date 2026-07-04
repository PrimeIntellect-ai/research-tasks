You are a QA engineer tasked with setting up a robust test environment for a new request validation library. The project uses Rust and involves computing checksums, property-based testing, and conditional builds for benchmarking.

Create a Rust project in `/home/user/req_validator` and implement the following requirements:

1. **Library Implementation (`src/lib.rs`)**:
   - Write a public function `compute_checksum(payload: &[u8]) -> u8`.
   - The checksum must be calculated as the bitwise XOR sum of all bytes in the payload. However, any null byte (`0x00`) must be explicitly ignored/skipped during the calculation.

2. **Property-Based Testing**:
   - Add `proptest` as a `dev-dependency` in your `Cargo.toml`.
   - In `src/lib.rs`, create a test module containing a property-based test named `proptest_checksum_property` using the `proptest!` macro.
   - The property to test is: For any randomly generated valid `Vec<u8>` payload, if you compute its checksum, append that checksum byte to the end of a copy of the payload, and then compute the checksum of this new combined payload, the final result must always equal `0x00`.

3. **Conditional Builds & Main Executable (`src/main.rs`)**:
   - In `Cargo.toml`, define a feature named `bench_mode`.
   - Write a `main` function that reads a single line of string input from standard input (stdin), converts it to bytes, and computes its checksum using your library function.
   - The program should print the checksum in hexadecimal format exactly like this: `Checksum: 0xXX` (e.g., `Checksum: 0x0A` or `Checksum: 0x62` - zero-padded to 2 digits, lowercase hex letters are fine).
   - Use conditional compilation (`#[cfg(feature = "bench_mode")]`) so that if the program is compiled with the `bench_mode` feature enabled, it prints `Bench mode active` on a new line before or after the checksum. If the feature is not enabled, it should not print this line.

4. **Execution**:
   - Build and run the binary with the `bench_mode` feature enabled.
   - Feed the exact string `"HelloRust"` (without quotes, and do not include a trailing newline in the bytes passed to the checksum) via standard input to the program.
   - Save the standard output of this execution to `/home/user/bench_output.txt`.

Ensure your property tests pass when running `cargo test`.