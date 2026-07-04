You are tasked with building a C shared library and creating a Python-based testing harness for it using property-based testing. 

In `/home/user/url_parser`, there is a C project with a `CMakeLists.txt` and a source file `xss_check.c`. This library parses custom data structures to detect potential XSS payloads. It exposes the following C function and struct:

```c
struct Payload {
    char* content;
    int length;
    int has_xss;
};

void check_xss(struct Payload* p);
```

Your objectives are:
1. Write a shell script at `/home/user/run.sh` that performs the following steps:
   - Creates a `build` directory inside `/home/user/url_parser` and navigates into it.
   - Uses CMake to configure the project and `make` to compile it. The compilation will produce a shared library named `libxss_check.so`.
   - Sets the appropriate environment variable (`LD_LIBRARY_PATH`) so that the Python script can locate the compiled shared library dynamically at runtime.
   - Executes a Python script `/home/user/test_xss.py` (which you must write) and redirects its standard output and standard error to `/home/user/report.txt`.

2. Write the Python script `/home/user/test_xss.py` that:
   - Uses the `ctypes` module to load `libxss_check.so`.
   - Defines a custom `ctypes.Structure` named `Payload` that exactly mirrors the C struct.
   - Sets the correct `argtypes` and `restype` for the `check_xss` function.
   - Uses the `hypothesis` library's `@given` decorator and `strategies.text()` to perform property-based testing on the `check_xss` function.
   - For each generated string, encodes it to bytes, populates the `Payload` struct (with the bytes, its length, and initializing `has_xss` to 0), and calls `check_xss`.
   - Asserts that `has_xss` is either `0` or `1` after the function returns.
   - Include a main block that runs the test function so it executes when the script is run directly.

Ensure `/home/user/run.sh` is executable (`chmod +x`). All file paths in your scripts should be absolute where appropriate or correctly relative to the working directory.