You are an open-source maintainer reviewing a broken Pull Request (PR) for a mathematical expression evaluation library. A contributor has submitted a PR that provides a fast Python wrapper around a vendored C-based math interpreter called `tinyexpr`.

The PR files are located in `/app/tinyexpr-py` and the vendored C project is in `/app/tinyexpr`. 

The contributor claims their implementation is much faster than Python's native `eval()` for large mathematical arrays, but the PR is currently failing tests and benchmarks. Specifically:
1. Mathematical evaluations are returning wildly incorrect or truncated values.
2. The benchmark is failing to show the expected >10x speedup over pure Python.
3. The automated test fixture for a custom mathematical function emulator is broken.

Your task is to fix the PR and successfully run the benchmark. Here are your requirements:

1. **Shared Library Management**: The contributor modified `/app/tinyexpr/Makefile` to build a shared library (`libtinyexpr.so`). You must fix any compilation bottlenecks or misconfigurations in this Makefile so that the library is built with maximum performance for the benchmark.
2. **ABI Configuration**: The Python wrapper in `/app/tinyexpr-py/te_wrapper.py` uses `ctypes` to interface with `libtinyexpr.so`. Fix the ABI bindings (argument types, return types) so that the interpreter correctly handles double-precision floating-point numbers without truncation or memory corruption.
3. **Test Fixtures**: Fix the mock setup in `/app/tinyexpr-py/test_te.py`. The test tries to emulate an injected variable by passing custom state to the interpreter, but the fixture setup is incomplete. Ensure `pytest /app/tinyexpr-py/test_te.py` passes completely.
4. **Integration and Benchmarking**: Once the tests pass, run `python /app/tinyexpr-py/benchmark.py`. This script will evaluate 100,000 mathematical expressions using both Python's `eval()` and the fixed `tinyexpr` wrapper. It will output a file at `/app/tinyexpr-py/results.json`.

Ensure your fixes allow `results.json` to be generated. The benchmark will calculate the Mean Squared Error (MSE) between the Python and C implementations, and the execution speedup. Your final solution must achieve an MSE of less than 1e-7 and a speedup threshold of at least 10.0x. Do not modify the `benchmark.py` file to fake the results, as your code will be evaluated using an independent verifier.