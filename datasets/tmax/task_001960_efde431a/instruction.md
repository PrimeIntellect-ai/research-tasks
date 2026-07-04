You are an engineer porting a custom web security tool (`http_fuzzer`) to work in a minimal Linux container. The tool consists of a C frontend and a Rust-based HTTP payload generator library. 

Currently, the project is broken and fails to build. You need to fix it and verify its functionality.

Here are your objectives:
1. **Fix the Rust ownership bug:** The payload generator library is located in `/home/user/tool/rust_parser`. There is a memory safety/ownership bug in `/home/user/tool/rust_parser/src/lib.rs` preventing it from compiling. Fix the bug so that the `get_fuzz_payload` function safely returns a pointer to a null-terminated static C string `"FUZZ_PAYLOAD_X99\0"`.
2. **Fix the C linking error:** The project's build system is driven by `/home/user/tool/Makefile`. The polyglot build orchestrates compiling the C code and the Rust static library, but it currently fails with "undefined reference" errors due to incorrect ordering of objects and archives in the linking step. Fix the `Makefile` so `make` successfully produces the `/home/user/tool/http_fuzzer` executable.
3. **Run the End-to-End test:** The tool needs to be tested against a minimal reverse proxy setup. We have provided an E2E orchestration script at `/home/user/tool/e2e_test.sh`. This script spins up a mock backend server and a reverse proxy, then runs your compiled `http_fuzzer` against it. Run this script and redirect its standard output to `/home/user/test_result.log`.

Constraints:
- Do not change the function signature of `get_fuzz_payload` in the Rust library or C file.
- Do not use dynamic linking for the Rust library (keep it as a `.a` static library).
- Your final output must be the successful execution log saved in `/home/user/test_result.log`.