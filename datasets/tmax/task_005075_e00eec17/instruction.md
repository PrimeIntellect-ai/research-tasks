You are a release manager preparing deployment tooling for a hybrid infrastructure consisting of high-performance servers and resource-constrained edge IoT devices. 

Your task is to build a high-performance, zero-allocation C parser for a custom "Release Manifest" format, configure a build system to conditionally compile it for different environments, and benchmark its performance.

All work should be done in `/home/user/workspace/`.

### 1. The Parser (C)
Create a file at `/home/user/workspace/manifest_parser.c`.
This program must parse a manifest file provided as the first command-line argument.
The parser **must** be implemented as a byte-by-byte state machine (e.g., using an `enum` of states and a `switch` statement). Do not use regex or high-level string splitting functions.

**Manifest Format:**
Each line represents a package and follows this exact format:
`[<Type>] <Name> v<Version>\n`

*   `Type`: Must be exactly `APP`, `LIB`, or `SYS`.
*   `Name`: 1 to 64 characters consisting only of lowercase letters, numbers, and dashes (`-`).
*   `Version`: Must be strictly `X.Y.Z` where X, Y, and Z are integers from 0 to 999.
*   The file ends with a newline.

### 2. Conditional Builds
The C code must handle two distinct compilation modes via preprocessor macros:
*   **SERVER_MODE**: When compiled with `-DSERVER_MODE`, the program should validate the file and, if perfectly valid, print exactly: `SUCCESS: Parsed <N> packages.` to `stdout` (where `<N>` is the integer count of packages), then exit with code `0`.
*   **EDGE_MODE**: When compiled with `-DEDGE_MODE`, the program must omit all `stdout` printing to save binary size/IO. It should only validate the file and exit with code `0` on success.
*   **Error Handling (Both modes)**: If *any* syntax error, invalid type, or length violation is encountered, the program must immediately exit with code `1`.

### 3. Build System
Create `/home/user/workspace/Makefile`.
It must define the following targets:
*   `server`: Compiles `manifest_parser.c` into an executable named `parser_server` using `SERVER_MODE`, optimized with `-O3`.
*   `edge`: Compiles `manifest_parser.c` into an executable named `parser_edge` using `EDGE_MODE`, optimized for size with `-Os`.
*   `clean`: Removes the compiled binaries.

### 4. Benchmarking Script
Create a bash script at `/home/user/workspace/benchmark.sh`.
This script must:
1. Generate a mock manifest file named `large_manifest.txt` containing exactly 50,000 valid package lines.
2. Compile both binaries using your Makefile.
3. Use the bash `time` command to measure the execution time of both `parser_server` and `parser_edge` parsing `large_manifest.txt`.
4. Append the word `DONE` to a file named `/home/user/workspace/benchmark_results.txt` when the benchmarking is complete.

Make sure your code handles potential edge cases like missing newlines at the end of the file or invalid characters gracefully by returning exit code 1.