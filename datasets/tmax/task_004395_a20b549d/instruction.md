You are a web developer working on a high-performance backend feature that processes incoming HTTP request paths. To maximize performance and code reuse, the team uses a polyglot approach: a low-level C library for string parsing, and a C++ core for business logic. We also need to build two versions of this core: a native executable for the server backend, and a web-targeted executable (simulated here via preprocessor flags) for edge deployment.

You have been given a workspace at `/home/user/backend_feature` containing:
- `libparser.c` and `libparser.h` (C library for parsing)
- `processor.cpp` (C++ application logic)
- `build.py` (A skeleton build script)

However, the current code has a memory leak, and the build script is incomplete. 

Your tasks are:
1. **Memory Debugging:**
   - Compile the current code into a temporary executable.
   - Run Valgrind on it to detect the memory leak.
   - Redirect the standard error of the Valgrind run to `/home/user/valgrind_report.txt`.

2. **Fix the Leak:**
   - Modify `/home/user/backend_feature/processor.cpp` to fix the memory leak. The leak originates from memory allocated in the C library that is not freed in the C++ code. Make sure to include any necessary headers.

3. **Polyglot Build Orchestration & Conditional Builds:**
   - Complete `/home/user/backend_feature/build.py` so that it automatically performs the following steps when executed:
     a) Compiles `libparser.c` into an object file `libparser.o` using `gcc`.
     b) Compiles and links `processor.cpp` with `libparser.o` to create an executable named `processor_native`, defining the macro `TARGET_NATIVE` during compilation (using `g++`).
     c) Compiles and links `processor.cpp` with `libparser.o` to create an executable named `processor_web`, defining the macro `TARGET_WEB` during compilation (using `g++`).
   - Execute your completed `build.py` script so that `processor_native` and `processor_web` are generated in `/home/user/backend_feature`.

When finished, the automated tests will run Valgrind on your compiled `processor_native` to ensure the memory leak is resolved. It will also execute `processor_web` to verify conditional compilation.