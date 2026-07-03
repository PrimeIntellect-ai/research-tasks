You are acting as a build engineer managing our artifact pipeline. We have a two-stage artifact validation system written in C and Rust, but both tools are currently broken and failing our CI pipeline. 

Your task is to fix the memory safety issues in the C program, fix the borrow checker errors in the Rust program, compile both, and run them on a provided binary artifact to generate a final verification report.

Here is the setup of your environment:
1. `/home/user/src/parser.c` - A C program that deserializes a binary artifact header. It currently suffers from Undefined Behavior (UB), a double-free, and a missing null-terminator when reading strings.
2. `/home/user/src/verifier.rs` - A Rust program that computes a checksum on the deserialized metadata to verify integrity. It currently fails to compile due to ownership and borrow checker errors.
3. `/home/user/artifacts/app_v1.bin` - The binary artifact you need to process.

**Step 1: Fix the C Parser**
The `parser.c` tool reads a binary file where the first 4 bytes (little-endian integer) represent the length of the metadata string, followed by the string itself. 
Fix the C code so that it:
- Correctly allocates enough memory for the string AND a null-terminator.
- Safely prints the extracted string to `stdout` in the format: `METADATA: <string>`
- Eliminates any memory leaks or double-frees.

**Step 2: Fix the Rust Verifier**
The `verifier.rs` takes a single command-line argument (the metadata string extracted by the C parser) and computes a simple 16-bit additive checksum. 
Fix the Rust code so that it compiles. You must resolve the borrow checker issue where the `String` is moved into the `compute_checksum` function but is later used. Do not change the underlying checksum algorithm.

**Step 3: Build and Execute**
Compile the C program to `/home/user/bin/parser` (using `gcc`).
Compile the Rust program to `/home/user/bin/verifier` (using `rustc`).

Finally, write a shell pipeline or script that runs the parser on `/home/user/artifacts/app_v1.bin`, extracts the metadata string, passes it as an argument to the verifier, and saves the combined output into a log file at `/home/user/artifact_report.txt`.

The final `/home/user/artifact_report.txt` must contain exactly two lines:
1. The output from the C parser.
2. The output from the Rust verifier.

Ensure your code is robust and compiles without warnings.