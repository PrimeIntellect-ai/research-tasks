You are an engineer tasked with fixing a vendored C library and integrating it into a new polyglot poly-service using a Bash-based request handler. 

A third-party matrix operations package is vendored at `/app/libmatrix-0.1.0`. This package builds a shared library used via Foreign Function Interface (FFI) by a provided Python script (`ffi_caller.py`). However, the package is currently broken, contains a memory safety vulnerability, and is extremely slow. 

Your tasks are:

1. **Fix the Build System**: The `Makefile` in `/app/libmatrix-0.1.0` is misconfigured and fails to correctly produce a dynamically linkable shared object (`libmatrix.so`). Fix the compiler and linker flags so that `make` successfully builds `libmatrix.so`.

2. **Repair Memory Safety & Optimize**: 
   - The C implementation in `src/matrix_ops.c` contains an undefined behavior (an off-by-one out-of-bounds array access during matrix multiplication). Find and fix this memory safety issue.
   - The matrix multiplication loop is extremely cache-inefficient (currently $O(N^3)$ with poor spatial locality). Reorder the loops to significantly improve CPU cache utilization (e.g., the standard `i, k, j` optimization). Your optimized implementation must execute in under **0.5 seconds** for 500x500 matrices (the unoptimized version takes much longer).

3. **Build the Handler Script**: 
   Write a Bash script at `/home/user/service.sh` that acts as the entrypoint for our service. It must accept exactly two arguments (paths to two matrix files). 
   - **Request Validation**: Verify that exactly two arguments are provided, both files exist, and are strictly greater than 0 bytes. If validation fails, print `ERROR: INVALID_REQUEST` to stdout and exit with code 1.
   - **Rate Limiting**: Implement a strict rate limit. The service must allow a maximum of **3 requests per 10-second rolling window**. If a request exceeds this limit, print `ERROR: RATE_LIMIT_EXCEEDED` to stdout and exit with code 429. (You may use standard CLI tools, temporary files, or directories to track timestamps).
   - **Execution**: If the request is valid and within the rate limit, the script must invoke the provided FFI caller: `python3 /app/libmatrix-0.1.0/ffi_caller.py <file1> <file2>` and pass through its stdout.

4. **Integration Setup**: Compile the shared library and ensure `/home/user/service.sh` is executable and works correctly.

Ensure your `service.sh` relies purely on Bash built-ins and standard Linux utilities (e.g., `date`, `grep`, `wc`, `mkdir`).