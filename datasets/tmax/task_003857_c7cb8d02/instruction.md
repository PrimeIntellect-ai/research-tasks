You are a QA engineer setting up a test environment to validate a custom metrics tracking library alongside an expression evaluator. 

You have been provided with two files in `/home/user/`:
1. `metrics.c` - A C source file containing a function `void record_metric(double val)` that records metrics.
2. `data.bin` - A binary file containing mathematical expressions. This file is encoded in UTF-16LE.

Your task is to write and execute a test pipeline that does the following:
1. **Build the C library**: Compile `/home/user/metrics.c` into a shared library named `/home/user/libmetrics.so`.
2. **Read and Decode**: Read the expressions from `/home/user/data.bin`, correctly decoding them from UTF-16LE into standard strings.
3. **Parse and Evaluate**: Evaluate each mathematical expression to a floating-point number.
4. **FFI Integration**: Use Foreign Function Interface (FFI) in the language of your choice (e.g., Python's `ctypes`) to load `/home/user/libmetrics.so` and pass each evaluated result to the `record_metric(double)` C function.
5. **Output**: Save the successfully evaluated results (as standard strings, one per line) to `/home/user/eval_results.txt`.
6. **Memory Debugging**: The C library is suspected of having a memory leak. Run your evaluation script under `valgrind` with the `--leak-check=full` option. Redirect valgrind's standard error stream to `/home/user/valgrind.log`.

Ensure all output files (`eval_results.txt`, `valgrind.log`, and the library's internal output `metrics.out`) are generated in `/home/user/` with the exact names specified.