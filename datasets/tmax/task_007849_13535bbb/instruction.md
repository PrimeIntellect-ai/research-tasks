You are helping organize and test a legacy C library used for generating secure, tamper-evident checksums for web tokens. 

Currently, all files are dumped in the `/home/user/websec_project` directory. You need to reorganize the project, build a shared library with a strict ABI, and write a property-based test.

Here is the setup information:

1. **Initial Files:**
   In `/home/user/websec_project/`, there are two files.
   `checksum.c`:
   ```c
   #include "checksum.h"
   
   // Internal helper - MUST NOT be accessible from outside the shared library
   unsigned int internal_mix_entropy(unsigned int hash, char c) {
       return (hash << 5) + hash + c;
   }
   
   // Public API - MUST be accessible from the shared library
   unsigned int generate_web_token_hash(const char* input) {
       unsigned int hash = 5381;
       int c;
       while ((c = *input++)) {
           hash = internal_mix_entropy(hash, c);
       }
       return hash;
   }
   ```
   
   `checksum.h`:
   ```c
   #ifndef CHECKSUM_H
   #define CHECKSUM_H
   unsigned int generate_web_token_hash(const char* input);
   #endif
   ```

2. **Project Organization:**
   Reorganize the project by creating the following directories inside `/home/user/websec_project/` and moving files appropriately:
   - `src/` (move `checksum.c` here)
   - `include/` (move `checksum.h` here)
   - `lib/` (for the compiled shared library)
   - `tests/` (for test source files and executables)

3. **Shared Library & ABI Management:**
   Modify the source code or compilation flags as needed to compile `checksum.c` into a shared library named `libwebsec.so` inside the `lib/` directory. 
   **Crucial ABI Requirement:** The function `generate_web_token_hash` must be exported as a dynamic symbol, but `internal_mix_entropy` MUST be hidden (not exported in the dynamic symbol table).

4. **Property-Based Testing:**
   Create a test file at `/home/user/websec_project/tests/prop_test.c`. This program must link against your `libwebsec.so` and perform a property-based test of the hash function.
   The test must generate 100 random alphanumeric strings (lengths between 5 and 20 characters). For each string, it must assert two properties:
   - **Determinism:** Calling `generate_web_token_hash` twice on the exact same string produces the exact same integer output.
   - **Non-zero:** The resulting hash is never equal to 0.
   
   If all 100 iterations pass, the program must print `PROPERTY_TEST_SUCCESS` to standard output. If any fail, it must return a non-zero exit code.

5. **Execution:**
   Compile the test into an executable at `/home/user/websec_project/tests/prop_test`. Run it, and redirect its standard output to `/home/user/websec_project/test_result.log`.

Complete these tasks. The automated test will verify the directory structure, the exported symbols in `libwebsec.so`, and the contents of `test_result.log`.