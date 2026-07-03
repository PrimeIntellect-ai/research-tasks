You are an open-source maintainer reviewing a pull request for `tinyvm`, a minimal stack-based virtual machine written in Rust. 

The project is located at `/home/user/tinyvm`. 

The PR added a new feature to allow the VM to accept bytecode as a Hexadecimal string over an FFI boundary. The PR author wrote a custom Hex decoder to avoid pulling in external dependencies and added a property-based test using the `proptest` crate to verify that the decoding and execution pipeline works. 

However, the CI is currently failing because the property-based test occasionally panics. Furthermore, the PR author failed to provide an example program using the new C runner.

The custom architecture is a simple stack machine with the following opcodes (1 byte each):
- `0x01` `<val>`: PUSH (pushes the next 1 byte onto the stack)
- `0x02`: ADD (pops two values, pushes their sum)
- `0x03`: SUB (pops `a`, pops `b`, pushes `b - a`)
- `0xFF`: HALT (pops the top of the stack and returns it as the execution result)

Your tasks to complete this PR review are:
1. Identify and fix the logic error in `/home/user/tinyvm/src/decoder.rs` so that `cargo test` passes consistently.
2. Build the Rust project in release mode to generate the shared library (`libtinyvm.so`).
3. Compile the provided C program `/home/user/tinyvm/runner.c`, linking it against the newly built shared library. The output executable should be named `runner`.
4. Hand-assemble a minimal program in `tinyvm` bytecode that performs the calculation: `25 + 35 - 10`.
5. Run the `runner` executable with your hand-assembled bytecode (as a single contiguous hex string) as its only argument.
6. Save the standard output of the `runner` command to `/home/user/result.log`.

Note: You may need to set `LD_LIBRARY_PATH` to ensure the C runner can find the shared library at runtime.