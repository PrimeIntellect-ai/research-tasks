You have been given a PyO3 project in `/home/user/project` that wraps a Rust function into a Python module named `data_processor`. The project currently fails to compile due to a syntax/type error in the Rust code.

Your objectives are:
1. Fix the compilation error in `/home/user/project/src/lib.rs`. The function `process_data` should take a list of integers, remove duplicates, sort them in ascending order, and return the new list.
2. Build the Python extension in the current virtual environment (or system environment) so it can be imported in Python. The project uses `maturin`.
3. Write a property-based test script at `/home/user/project/test_prop.py` using the `hypothesis` library. It should test `data_processor.process_data` with lists of integers. Verify that the output is exactly equivalent to Python's `sorted(list(set(input_list)))`. The script should exit with code 0 if successful.
4. Write a benchmarking script at `/home/user/project/benchmark.py` that generates a random list of 100,000 integers (between 0 and 100,000), runs `data_processor.process_data` on this list 50 times, and calculates the average execution time. Save the result to `/home/user/project/benchmark.json` in the exact format: `{"avg_time_sec": 0.123}`.
5. Write a memory profiling script at `/home/user/project/profile_mem.py` using Python's built-in `tracemalloc` module. The script should start tracemalloc, run `data_processor.process_data` on a random list of 500,000 integers, take a snapshot or get the peak memory usage, and write ONLY the peak memory usage (an integer representing bytes) to `/home/user/project/memory.txt`.

Ensure all Python scripts run successfully and produce the required output files.