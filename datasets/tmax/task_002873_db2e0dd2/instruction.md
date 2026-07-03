You are a platform engineer maintaining the CI/CD pipelines for your company's infrastructure team. A critical security policy evaluator written in Go has broken the build pipeline due to a recent commit. 

The source code is located at `/home/user/sec-eval`. The tool parses and evaluates basic boolean security expressions. 

Your tasks are:

1. **Fix the Build (Circular Import):**
   The project currently fails to build due to a circular import between the `parser` and `eval` packages. 
   Refactor the code to resolve this issue. The simplest method is to merge the contents of `parser` and `eval` into a single new package called `engine`. Update `main.go` and any necessary references so the tool builds successfully. Do not change the underlying logic or exit codes.

2. **Cross-Compilation:**
   Cross-compile the fixed Go application for two targets:
   - Linux (amd64): Output the binary to `/home/user/dist/sec-linux`
   - Windows (amd64): Output the binary to `/home/user/dist/sec-win.exe`
   (Make sure the `/home/user/dist` directory exists).

3. **Property-Based Testing (Multi-language):**
   We need to ensure the expression parser gracefully handles garbage input without crashing (panicking). The Go binary exits with `0` for valid expressions, `1` for safe parse/eval errors, and `2` if it panics.
   
   Install the `hypothesis` Python library (`pip install hypothesis`).
   Write a Python script at `/home/user/test_props.py` that uses `@given(strategies.text())` from `hypothesis` to generate random strings. 
   For each generated string, the script should use `subprocess.run` to execute `/home/user/dist/sec-linux` with the string as the only command-line argument.
   The test must assert that the return code of the process is **never** `2`. 
   
   Execute your Python test script. If it runs successfully without raising an `AssertionError`, write the exact string `"TESTS_PASSED"` to `/home/user/test_result.log`.