You are a build engineer managing a multi-language artifact pipeline for a data processing component. Your task is to conditionally compile a C component, cross-compile a Go component, and write a property-based test to ensure both compiled binaries exhibit identical behavior.

All your work will take place in `/home/user/artifacts`. 
The source files are already present in `/home/user/src`.

Here are your instructions:

1. **Polyglot & Conditional Build**:
   - Compile the C program `/home/user/src/processor.c` using `gcc`. You must pass the macro definition `ENABLE_REVERSE=1` during compilation for the program to behave correctly. Output the binary to `/home/user/artifacts/c_linux_amd64`.
   - Compile the Go program `/home/user/src/processor.go` natively for Linux (amd64). Output the binary to `/home/user/artifacts/go_linux_amd64`.

2. **Cross-Compilation**:
   - Cross-compile the same Go program `/home/user/src/processor.go` for Windows (amd64). Output the executable to `/home/user/artifacts/go_windows_amd64.exe`.

3. **Property-Based Testing**:
   - A partially complete Python script using the `hypothesis` library is located at `/home/user/src/test_props.py`.
   - Modify `/home/user/src/test_props.py` so that the `test_processors_match(input_str)` function uses Python's `subprocess` module to execute both native Linux binaries (`/home/user/artifacts/c_linux_amd64` and `/home/user/artifacts/go_linux_amd64`) passing `input_str` as the only command-line argument.
   - Assert that the standard outputs of both binaries are strictly equal.
   - Run the completed Python script. If the tests pass, the script is already configured to write "PROPERTY TESTS PASSED" to `/home/user/artifacts/test_report.txt`.

Ensure all artifact files (`c_linux_amd64`, `go_linux_amd64`, `go_windows_amd64.exe`, and `test_report.txt`) are exactly where specified. 

*Note: You may need to ensure `hypothesis` is available, e.g., via `pip install hypothesis` if not already installed. Assume standard compilers (`gcc`, `go`) are installed.*