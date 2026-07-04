You are acting as a senior developer debugging a failing nightly CI build for a custom C++ data parser. 

The CI build log is available at `/home/user/ci_log.txt`. It indicates that our libFuzzer job found a severe memory issue (an out-of-bounds read) resulting in a crash. However, the repository (`/home/user/parser_repo`) is missing some crucial testing pieces because a junior developer accidentally deleted the fuzzing dictionary file in a recent commit.

Your tasks are to combine git forensics, intermediate state tracing, and fuzzing to fix the code:

1. **Git Forensics & Recovery**: Inspect the git history of `/home/user/parser_repo`. Find the accidentally deleted fuzzing dictionary file (it was named `fuzz_dict.txt`). Extract the exact string token it contained and write it to `/home/user/recovered_token.txt`.
2. **Fuzzer Creation**: Write a libFuzzer harness named `fuzz_target.cc` inside `/home/user/parser_repo` that tests the `parse_data(const uint8_t* data, size_t size)` function defined in `parser.h`.
3. **Reproduction**: Compile your fuzzer with AddressSanitizer enabled:
   `clang++ -g -O1 -fsanitize=fuzzer,address fuzz_target.cc parser.cpp -o fuzzer`
   Run it to reproduce the intermediate state crash mentioned in the CI log.
4. **Fix the Bug**: Analyze the AddressSanitizer trace and the source code of `parser.cpp`. The bug occurs during the intermediate parsing state when the recovered token is encountered but the buffer isn't long enough for subsequent checks. Fix the vulnerability in `parser.cpp`.
5. **Verification**: Ensure your fixed `parser.cpp` compiles and the fuzzer can run for at least 50,000 iterations (`./fuzzer -runs=50000`) without any crashes or memory errors.

Leave the fixed `parser.cpp` and `fuzz_target.cc` in the repository, and ensure `/home/user/recovered_token.txt` contains the correct token string.