You are tasked with fixing and testing a multi-language project located at `/home/user/rust_calc`. 
The project is a Rust-based CLI calculator that applies predefined mathematical operations. However, it currently fails to compile because a crucial source file, `src/encoded_ops.rs`, is missing. This file is supposed to be generated dynamically from a custom binary file, `ops.dat`. 

Additionally, you must implement a robust property-based testing suite in Python to verify the compiled binary, while mocking a telemetry service the CLI attempts to contact.

Here are the specific requirements:

1. **Build Orchestration & Data Encoding:**
   Write a Python script at `/home/user/build_orchestrator.py` that reads `/home/user/rust_calc/ops.dat`. 
   The `ops.dat` file contains custom binary encoded records. Each record is exactly 4 bytes long:
   - Byte 0: `op_id` (unsigned 8-bit integer)
   - Byte 1: `op_type` (unsigned 8-bit integer: `0` represents Addition, `1` represents Subtraction)
   - Bytes 2-3: `const_val` (16-bit signed little-endian integer)
   
   Your Python script must parse this file and generate valid Rust code in `/home/user/rust_calc/src/encoded_ops.rs`. The generated Rust file must contain a single public function:
   `pub fn apply_op(op_id: u8, input: i32) -> i32`
   This function should use a `match` statement on `op_id` to either add or subtract `const_val` to/from `input`. If an unknown `op_id` is passed, it should return `input` unchanged.
   After generating the file, the Python script must invoke `cargo build` within the `/home/user/rust_calc` directory to compile the project.

2. **Property-Based Testing & Mock Setup:**
   Write a Python test suite at `/home/user/test_cli.py` using `pytest` and `hypothesis`.
   The compiled Rust binary will be located at `/home/user/rust_calc/target/debug/rust_calc`. It takes two arguments: `<op_id>` and `<input>` and prints the result to standard output.
   
   When executed, the Rust CLI also attempts to send a telemetry HTTP GET request to `http://localhost:8080/log`.
   Your Python test script must:
   - Set up a test fixture that spins up a mock HTTP server on port 8080 to gracefully accept these requests (returning 200 OK) so the CLI doesn't hang or crash.
   - Use `hypothesis` to write a property-based test checking that for `op_id = 1` (which you will discover from parsing `ops.dat` corresponds to an addition of 42), `apply_op(1, input) == input + 42` holds true for any integer `input` between -10000 and 10000.
   - Use `hypothesis` to test `op_id = 2` (subtraction of 15) ensuring `apply_op(2, input) == input - 15` for the same input range.

3. **Execution:**
   Run your build orchestrator, then run your test script using `pytest`.
   If the tests pass successfully, write the exact string `ALL_TESTS_PASSED` to `/home/user/success.log`.