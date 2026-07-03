I'm trying to organize a massive directory of legacy configuration files based on the result of the mathematical expressions inside them, and I also need to expose our proprietary math engine as an internal microservice.

I have a proprietary, stripped shared library located at `/app/libevaluator.so`. Even though it's stripped, it exports a single dynamic function used for evaluation. This function takes a standard C string (the mathematical expression) and returns a standard C `double` representing the result.

Your task:
1. **Analyze the Binary**: Inspect `/app/libevaluator.so` to find the exact name of the exported C function.
2. **Expose an API**: Use any language of your choice to write a script that loads this shared library via FFI (e.g., Python's `ctypes`, Node's `ffi`, etc.) and exposes it via an HTTP server listening on exactly `127.0.0.1:9090`. 
    - The server must handle `GET /calculate?expr=<expression>`.
    - It must return an HTTP 200 with the evaluated result as plain text (e.g., `42.5`).
    - The server must run continuously in the background so that it can be tested.
3. **Organize Files**: There is a directory `/home/user/configs` containing hundreds of `.txt` files. Each file contains a single math expression on the first line. 
    - Evaluate each file's expression using your FFI setup (or by calling your own API).
    - If the evaluated result is strictly greater than `100.0`, move that file to `/home/user/configs_high/`.
    - If it is less than or equal to `100.0` (or if it evaluates to an error/NaN), move it to `/home/user/configs_low/`.
4. **Benchmark**: Perform a quick benchmark of the FFI function. Evaluate the expression `"100 * 50 + 20"` 10,000 times natively via FFI. Write the total execution time in seconds (as a simple float, e.g., `0.045`) to `/home/user/benchmark.txt`.

Ensure your API is running and listening on `127.0.0.1:9090` when you are done. Create any output directories if they don't exist.