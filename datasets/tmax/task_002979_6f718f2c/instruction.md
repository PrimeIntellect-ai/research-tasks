You are an engineer working on a web security team. We are porting a high-performance Python-based custom authentication token parser, `fast-token-parser`, to work in our minimal CI container environment. 

The project uses a C extension for fast binary parsing. The test suite passes on the original developer's local machine, but crashes in our CI environment (which we are currently simulating). 

There are two distinct issues you need to resolve:
1. **Import Ordering Issue:** In `/home/user/fast-token-parser/test_suite.py`, the import ordering causes a state initialization issue under CI conditions. The module `config` must be imported *before* the `ffi_wrapper` module, otherwise the wrapper initializes with an unsafe default buffer size.
2. **Memory Safety Issue:** The C backend `/home/user/fast-token-parser/parser.c` contains a memory safety bug (buffer overflow) when handling malformed tokens. Specifically, the token format is `[1-byte type][2-byte length (Big Endian)][data]`. The C function `parse_token` uses a fixed 64-byte internal stack buffer. If the parsed length exceeds this, it overflows. You need to add a check in `parser.c` to cap the copied data to 64 bytes (or safely truncate it) and return a status code of `-1` if an overflow attempt is detected.

Your tasks:
1. Fix the import order in `/home/user/fast-token-parser/test_suite.py`.
2. Fix the memory safety bug in `/home/user/fast-token-parser/parser.c`.
3. Recompile the C extension using GCC:
   `gcc -shared -o libparser.so -fPIC parser.c`
   (Ensure `libparser.so` is in `/home/user/fast-token-parser/`).
4. Run the test suite: `python3 /home/user/fast-token-parser/test_suite.py`.

If successful, the test suite will successfully process all payloads and write the structured, parsed data to `/home/user/parsed_tokens.json`. Ensure this file is generated successfully.