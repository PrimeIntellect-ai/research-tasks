You are a systems programmer debugging a C project that parses and evaluates mathematical sequences encoded in hex strings. 

The project is located in `/home/user/math_project/` and contains the following files:
- `libmathparse.c`: A C source file for a shared library that parses a custom hex-encoded string format and calculates a sum.
- `libmathparse.h`: The header file for the library.
- `main.c`: A test program that passes a specific encoded mathematical sequence to the library and writes the result to a file.
- `Makefile`: The build script.

The project currently suffers from two distinct problems:
1. **Memory Safety & Undefined Behavior**: `libmathparse.c` contains a memory safety bug (a heap buffer overflow) during the parsing phase. The parsing logic reads the length of the data payload and then iterates through the hex string, but it writes out of bounds of the allocated buffer.
2. **Library Linking/Loading Issue**: The `Makefile` successfully compiles `libmain` but fails to appropriately configure the linker or runtime loader path. If you try to run `./main` after running `make`, the OS will fail to locate the shared library `libmathparse.so` at runtime.

Your tasks are to:
1. Identify and fix the memory safety issue (undefined behavior) in `/home/user/math_project/libmathparse.c`.
2. Fix the `Makefile` (or the runtime execution environment) so that `./main` successfully finds and loads `libmathparse.so` at runtime.
3. Build the project using `make`.
4. Run the executable `./main`.

If you succeed, the program will execute without crashing and automatically create a file at `/home/user/math_project/result.txt` containing the calculated output.