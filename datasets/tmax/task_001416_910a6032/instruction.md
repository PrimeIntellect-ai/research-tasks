You are an engineer tasked with setting up a polyglot build system and fixing a broken data processing tool. The tool is designed to read text files, validate their character encoding (ensuring strict UTF-8), and sanitize them by rejecting malicious payloads.

The project is located at `/home/user/polyglot-sanitizer`. It consists of a high-performance C library (`c_src/`) and a safe Rust CLI wrapper (`rust_src/`).

Currently, the project is completely broken:
1. **Build System Missing:** There is no build script to compile the C code into a shared library (`libfilter.so`) and link it to the Rust project.
2. **C Memory Safety & Undefined Behavior:** The C library (`c_src/filter.c`) contains memory leaks and a buffer overflow vulnerability when parsing certain multi-byte character encodings.
3. **Rust Ownership & ABI Issues:** The Rust wrapper (`rust_src/src/main.rs`) attempts to call the C library via FFI but fails to compile due to lifetime issues and incorrect handling of raw pointers.

Your objectives:
1. **Fix the C Code:** Debug and repair `c_src/filter.c` so it safely handles all inputs without leaking memory or reading out of bounds.
2. **Fix the Rust Code:** Resolve the borrow checker errors in `rust_src/src/main.rs`. Ensure memory returned by the C library is properly managed and freed if necessary across the FFI boundary.
3. **Create a Build Pipeline:** Write a bash script at `/home/user/polyglot-sanitizer/build.sh` that:
   - Compiles `filter.c` into a shared library (`libfilter.so`).
   - Configures the linker paths appropriately.
   - Compiles the Rust project in release mode.
   - Moves the final Rust executable to `/home/user/polyglot-sanitizer/bin/sanitizer_cli`.
4. **Validation:** The final binary must take a file path as its first CLI argument. It should exit with code `0` and print the sanitized text to standard output for valid files, and exit with code `1` (with no standard output) for invalid/malicious files.

**Resources Provided:**
- **Reference Oracle:** A stripped, UPX-packed binary is located at `/app/sanitizer_oracle`. This binary implements the exact validation and sanitization algorithm your polyglot tool is supposed to emulate. You can use it to determine the expected behavior for any given input.
- **Corpora:** 
  - `/app/corpus/clean/`: Contains valid text files. Your tool must exit `0` and preserve the text.
  - `/app/corpus/evil/`: Contains malformed encodings and exploit payloads. Your tool must exit `1`.

Your task is complete when your compiled binary at `/home/user/polyglot-sanitizer/bin/sanitizer_cli` successfully processes the provided corpora identically to the oracle binary.