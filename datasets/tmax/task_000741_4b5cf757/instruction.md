You are tasked with organizing the project files for a C-based HTTP REST API parser, configuring its build system, and debugging its internal state machine. 

Currently, all the files are dumped in a single directory: `/home/user/workspace`. Inside, you will find:
- `http_parser.c` (Contains a logic bug in the parser)
- `http_parser.h`
- `test_http_parser.c` (The test suite)

Your objectives are:

1. **Reorganize the Project**: Create a new directory `/home/user/api_parser`. Inside it, create three subdirectories: `src`, `include`, and `tests`. 
2. **Move the Files**:
   - Move `http_parser.c` to `/home/user/api_parser/src/`
   - Move `http_parser.h` to `/home/user/api_parser/include/`
   - Move `test_http_parser.c` to `/home/user/api_parser/tests/`
3. **Fix the State Machine**: The C code in `http_parser.c` implements a simple state machine to parse the HTTP method, path, and version from a request. However, it currently has a bug where it fails to extract the path correctly. Identify and fix the bug in `src/http_parser.c`. Do not modify `http_parser.h` or `test_http_parser.c`.
4. **Create a Build System**: Write a `Makefile` located exactly at `/home/user/api_parser/Makefile` with the following targets:
   - `libparser.a`: Compile `src/http_parser.c` into a static library. Ensure the compiler looks for headers in the `include/` directory.
   - `test_runner`: Compile `tests/test_http_parser.c` and link it against `libparser.a` to produce an executable named `test_runner`.
   - `test`: A target that builds `test_runner` (if not already built) and executes it. The standard output of the test runner must be redirected and saved to `/home/user/api_parser/test_summary.txt`.
   - `clean`: Removes all compiled object files, `libparser.a`, `test_runner`, and `test_summary.txt`.
5. **Run the Tests**: Execute your `test` target. If your fix and build system are correct, the file `/home/user/api_parser/test_summary.txt` will be created and should read exactly `ALL TESTS PASSED`.