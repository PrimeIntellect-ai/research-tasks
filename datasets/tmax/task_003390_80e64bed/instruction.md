You are helping a web developer build a native C backend service for processing custom encoded URL payloads. They have a basic prototype, but they are running into several issues with building, linking, and memory management.

You have been provided with a project in `/home/user/project/`. 
The project contains:
- `libdataparser.c` and `libdataparser.h`: A shared library that parses a custom key-value serialization format (e.g., `key1:value1,key2:value2`).
- `main.c`: The main application that uses the shared library.
- `Makefile`: The build script.

Currently, the developer is facing the following problems:
1. The `Makefile` is broken. It fails to link `libdataparser.so` when building the `app` executable because it cannot find the library at link time.
2. Even if it compiles, `main.c` has a memory leak when deserializing the payload.

Your task is to fix the project and create a Bash test-runner script:

1. Fix `/home/user/project/Makefile` so that running `make` successfully builds both `libdataparser.so` and `app`. Ensure the `app` target properly depends on the shared library and links correctly against it from the current directory.
2. Fix the memory leak in `/home/user/project/main.c` so that all allocated memory from the parser is correctly freed before the program exits. (Do not change the behavior or standard output of the program).
3. Write a Bash testing script at `/home/user/project/run_tests.sh`. The script must:
   - Be executable.
   - Accept exactly one argument: the payload string to test.
   - Set up the environment so that the `app` executable can find `libdataparser.so` at runtime.
   - Run the `app` executable with the provided payload argument using `valgrind`.
   - Configure Valgrind to check for memory leaks (`--leak-check=full`) and to exit with a non-zero code (specifically 1) if any memory errors or leaks are detected (`--error-exitcode=1`).
   - Redirect the standard output of `app` to `/home/user/project/output.log`.
   - The script must exit with the exact same exit code returned by the Valgrind command.

When you are finished, I should be able to run `/home/user/project/run_tests.sh "role:admin,id:404"` and it should return an exit code of `0` while populating `/home/user/project/output.log` with the parsed output.