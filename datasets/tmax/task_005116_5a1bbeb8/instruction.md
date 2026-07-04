You are a systems programmer debugging a C library compatibility issue. 

In `/home/user/project`, you have an application `app` that dynamically links against `libstatemachine.so`. The application contains a state machine parser that has two code paths:
- A "slow path" used for library versions 1.x.
- A "fast path" (V2 path) that is only activated if the library's semantic version is `2.0.0` or higher.

The current system library (`libstatemachine.so`) is hardcoded to version `1.5.0`, so the application defaults to the slow path. We suspect there is a memory leak specifically within the V2 fast path of the `app` binary.

Your task is to isolate and profile this memory leak without modifying or recompiling the `app` binary or the original `libstatemachine.so`.

Perform the following steps:
1. Create a C file and compile it into a mock shared library at `/home/user/project/libmock.so`. Your mock must intercept the function `const char* sm_get_version()` and return `"2.1.0"` to trick the application into taking the V2 fast path.
2. Use `LD_PRELOAD` to load your mock alongside the `app` executable.
3. Use `valgrind` (with `--leak-check=full`) to run the `app` with the mock injected.
4. Identify the exact number of bytes that are reported as "definitely lost" by Valgrind.
5. Create a file named `/home/user/project/leak_size.txt` containing ONLY the integer number of definitely lost bytes.

Do not recompile `app` or `libstatemachine.so`. Your mock should only override the version check; the actual processing function `sm_process` should still be resolved from the original `libstatemachine.so`.