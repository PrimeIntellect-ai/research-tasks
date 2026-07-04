You are a platform engineer responsible for maintaining your company's CI/CD pipeline for a custom Web Application Firewall (WAF) rule evaluator. 

The pipeline is currently failing due to multiple issues across our polyglot codebase. The security scanner relies on a high-performance Rust library to sanitize incoming HTTP payloads (character encoding/decoding), and a Python script that acts as an emulator to evaluate a proprietary bytecode representing suspicious execution patterns.

Your workspace is located at `/home/user/waf_pipeline`. 

You need to perform the following steps to fix the pipeline:

1. **Fix the Rust Borrow Checker Error:**
   The Rust data sanitizer located in `/home/user/waf_pipeline/rust_sanitizer/src/lib.rs` fails to compile due to a strict ownership/borrowing bug. The function `sanitize_payload` is meant to inspect a byte slice, modify the underlying vector to append a null terminator, and then log the first few bytes. Fix the borrow checker error without changing the function's signature or external C-API behavior.

2. **Fix the Python Emulator:**
   The Python WAF emulator script is located at `/home/user/waf_pipeline/python_scanner/vm.py`. It implements a tiny stack-based virtual machine to analyze payloads. The `XOR` instruction (opcode `0x03`) is missing its implementation. Implement it. It should pop the top two values from the stack, perform a bitwise XOR, and push the result back onto the stack.

3. **Orchestrate the Polyglot Build:**
   Create a bash script at `/home/user/waf_pipeline/build_and_run.sh` that does the following:
   - Compiles the Rust project in release mode (`cargo build --release` inside `rust_sanitizer`).
   - Copies the resulting shared library (`librust_sanitizer.so`) into the `python_scanner` directory.
   - Runs the python script: `python3 /home/user/waf_pipeline/python_scanner/scanner.py`.
   - Ensure the bash script is executable.

4. **Run the Pipeline:**
   Execute your `build_and_run.sh` script. The `scanner.py` will read a Base64 encoded test payload, pass it to the Rust library for sanitization, and then execute the result in the Python VM. It writes the final stack output to `/home/user/waf_pipeline/scan_result.log`.

**Expected End State:**
- `/home/user/waf_pipeline/rust_sanitizer/src/lib.rs` compiles successfully.
- `/home/user/waf_pipeline/python_scanner/vm.py` has the XOR logic.
- `/home/user/waf_pipeline/build_and_run.sh` is an executable script that builds and orchestrates the components.
- `/home/user/waf_pipeline/scan_result.log` contains the final output string from the emulator.