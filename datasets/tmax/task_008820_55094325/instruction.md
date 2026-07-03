You are a QA engineer setting up a test environment for a hybrid C++/Python data processing pipeline. The pipeline uses a C++ shared library for fast numerical computations (specifically, a moving average filter), which is called from Python via `ctypes`.

However, the current code in `/home/user/pipeline` is broken:
1. **Polyglot Build Orchestration & Linking:** The `Makefile` has errors. When you run `make`, it fails to produce a usable shared library (`libfilter.so`) because it is missing the necessary compiler and linker flags for creating a position-independent shared object in Linux. Fix the `Makefile` and successfully build `libfilter.so`.
2. **Memory Debugging:** The C++ implementation in `filter.cpp` contains a memory leak. Fix the memory leak in the C++ code. You have been provided a test driver `test_runner.cpp` which is built by the `Makefile`. Run this executable under `valgrind` with the `--leak-check=full` flag, and redirect the valgrind output (stderr) to `/home/user/pipeline/valgrind.log`.
3. **FFI & Benchmarking:** Once the C++ library is built and leak-free, run the provided Python script `/home/user/pipeline/benchmark.py`. This script loads your shared library via `ctypes` and benchmarks it against a pure Python implementation. Save the standard output of this script to `/home/user/pipeline/benchmark_result.txt`.

**Expected End State:**
- The `Makefile` is fixed, and `libfilter.so` is successfully built.
- The C++ file `filter.cpp` is modified to remove the memory leak.
- `/home/user/pipeline/valgrind.log` exists and contains proof that 0 bytes were leaked.
- `/home/user/pipeline/benchmark_result.txt` exists and contains the output of `benchmark.py`.

Please begin.