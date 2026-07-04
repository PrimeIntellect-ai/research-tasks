You are helping migrate a legacy data processing pipeline from Python 2 to Python 3. The pipeline consists of a Python script that delegates heavy mathematical computations to a custom C extension. 

However, we have encountered several critical issues during the migration:
1. The Python code relies on Python 2 syntax and standard libraries that have changed or been removed in Python 3.
2. The C extension (`fast_math.c`) has historically suffered from silent memory leaks and Undefined Behavior (specifically an out-of-bounds array read). In Python 2, this occasionally worked by chance, but in Python 3 it causes erratic crashes and rapid memory exhaustion.
3. We need a new automated way to benchmark the fixed pipeline to ensure it meets our performance targets.

Your workspace is located at `/home/user/legacy_app/`.
You will find the following files there:
- `main.py`: The Python 2 script.
- `fast_math.c`: The C extension source code containing the memory leak and UB.
- `setup.py`: The build script for the C extension.

Your objectives:
1. **Fix the C Extension**: Modify `fast_math.c` to repair the memory leak and the out-of-bounds buffer read (Undefined Behavior).
2. **Migrate to Python 3**: Refactor `main.py` so that it is fully compatible with Python 3.
3. **Orchestrate and Benchmark**: Write a Python 3 script named `/home/user/legacy_app/test_and_bench.py` that does the following:
   - Programmatically builds the C extension (e.g., via `subprocess` calling `python3 setup.py build_ext --inplace`).
   - Imports the newly built `fast_math` module and the refactored `main` module.
   - Runs an end-to-end benchmark by passing a list of 100,000 floats (from `0.0` to `99999.0`) into `fast_math.compute_sum()`.
   - Measures the execution time of this computation averaged over 100 iterations.
   - Verifies that the process does not leak memory (you may use the `resource` module or check `ps` memory usage before and after 1,000 iterations to ensure it stays bounded).
   - Writes a JSON file to `/home/user/legacy_app/migration_results.json` strictly matching this schema:
     ```json
     {
       "build_success": true,
       "python3_compatible": true,
       "average_execution_time_seconds": <float>,
       "memory_leak_fixed": true,
       "sum_result": <float>
     }
     ```

Ensure all files are saved in `/home/user/legacy_app/`. The automated test will run `python3 test_and_bench.py` and inspect the resulting `migration_results.json` and the source files.