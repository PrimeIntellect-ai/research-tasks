You are a systems programmer debugging a dynamic linking issue and memory leak within a minimal CI/CD environment. 

In `/home/user/project`, there is a C project containing a main application (`app`) and a shared library (`libcustom.so`). The application frequently fails in the CI pipeline because the runtime linker cannot find the custom library, and there are suspected memory leaks inside the library's data structures.

Your task is to write a Bash CI runner script at `/home/user/project/ci_runner.sh` that validates inputs, fixes the linking environment, and performs memory profiling.

Requirements for `/home/user/project/ci_runner.sh`:
1. **Request Validation**: The script must take exactly one argument: the path to the executable to test. If no argument is provided, or if the provided file is not executable, the script must print an error and exit with status code `1`.
2. **Build**: Run `make` in the `/home/user/project` directory to ensure the project is built.
3. **Environment Fix & Linking Verification**: The executable needs `libcustom.so` at runtime. Ensure the script configures the environment (e.g., `LD_LIBRARY_PATH`) so the dynamic linker can find the shared object located in the same directory.
4. **Memory Profiling**: Run the provided executable using `valgrind --leak-check=full`. You must capture its standard error output to analyze the memory leak.
5. **Report Generation**: Parse the valgrind output and create a test report at `/home/user/project/ci_report.txt`. 
   The report must contain exactly two lines:
   - Line 1: `LINKING: SUCCESS` (you can assume success if valgrind runs the program successfully).
   - Line 2: `LEAKED_BYTES: <N>` where `<N>` is the exact integer number of bytes reported as "definitely lost" by Valgrind.

Once you have written the script, execute it against the compiled `app` to generate the `ci_report.txt` file.

Make sure your script is executable (`chmod +x`).