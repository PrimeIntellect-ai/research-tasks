You are tasked with fixing and securing a multi-file Rust project called `msg_gateway` located at `/home/user/msg_gateway`. This project acts as an FFI bridge to a legacy C library, `libmsgparse`, which is used for parsing proprietary binary messages. 

Currently, the project is in a broken state:
1. **Compilation Failure**: The project fails to compile. The C library is vendored at `/app/libmsgparse-1.2.0`. Its `Makefile` has been corrupted by a bad merge, preventing it from producing a usable shared library (`libmsgparse.so`). Furthermore, the Rust project's `build.rs` might need adjustments to correctly link against it.
2. **Memory Safety / Undefined Behavior**: The legacy C library's parsing function blindly trusts the length headers in the binary messages. If given malformed data, it reads out of bounds and segfaults.

Your objectives are:

**Step 1: Fix the Build**
Navigate to `/app/libmsgparse-1.2.0` and fix the `Makefile` so that running `make` successfully compiles `libmsgparse.so`. 
Then, fix `/home/user/msg_gateway/build.rs` so that `cargo build` succeeds.

**Step 2: Secure the FFI Boundary**
In `/home/user/msg_gateway/src/main.rs`, implement the input validation logic *before* the C FFI is called. 
The proprietary binary message format is:
- Byte 0: Message Type (1 byte)
- Bytes 1-2: Payload Length (2 bytes, Big Endian)
- Bytes 3..: Payload Data

The Rust validation code must ensure that the total size of the file exactly matches `3 + Payload Length`. If the file is too short or too long, the program must gracefully print an error and terminate with exit code `1`. If the file is perfectly valid, it should pass the data to the C library, which will parse it, and the program should exit with code `0`.

**Step 3: Verify against Corpora**
We have provided two sets of binary files to test your implementation:
- `/app/corpora/clean/`: Contains perfectly well-formed messages.
- `/app/corpora/evil/`: Contains malformed messages designed to trigger out-of-bounds reads or segfaults in the C library.

Your Rust CLI tool must take a single file path as an argument.
Example: `cargo run -- /app/corpora/clean/msg1.bin`

When evaluating your solution, an automated verifier will invoke your compiled Rust binary against all files in both corpora. To pass, your program must exit with code `0` for all files in the `clean` corpus, and gracefully exit with code `1` (without crashing/segfaulting) for all files in the `evil` corpus.