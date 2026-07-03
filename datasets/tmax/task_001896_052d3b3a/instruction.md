You are tasked with fixing and completing a data processing utility written in Rust. We are migrating an old proprietary rolling-hash tool to Rust, and the current codebase in `/home/user/hash_util` is failing to compile due to ownership and borrow checker errors in its custom RingBuffer implementation. 

Additionally, the original developers left the crucial algorithmic parameters (the multiplier and the prime modulo) in a scanned specification image located at `/app/params.png`. 

Your objectives are:
1. Extract the missing `MULTIPLIER` and `MODULO` integer values from the specification image at `/app/params.png`. Tesseract OCR is installed on your system.
2. Fix the borrow checker and lifetime errors in the Rust project located at `/home/user/hash_util`. Do not change the overall architecture of the `RingBuffer` or the `RollingHash` structs, just fix the Rust-specific memory safety definitions.
3. Update the constants in `src/main.rs` with the values extracted from the image.
4. Compile the project using `cargo build --release`. 

The final executable must read raw bytes from `stdin` until EOF, process them through the rolling hash algorithm (which calculates a cumulative hash of sliding windows and combines them), and print the final 64-bit integer hash as a lowercase hex string to `stdout`.

The verifier will test your compiled binary against a stripped reference implementation by feeding both with identical random fuzz inputs and asserting bit-exact identical outputs. Ensure your final binary is located at `/home/user/hash_util/target/release/hash_util`.