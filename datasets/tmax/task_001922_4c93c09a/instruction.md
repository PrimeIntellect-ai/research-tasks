You are a performance engineer analyzing a Python script at `/home/user/calc_series.py`. This script is supposed to calculate a mathematical series concurrently over a large range of integers. However, during profiling and log analysis, you noticed two major issues:

1. The `process_number` function occasionally raises a `ZeroDivisionError` for a specific, undocumented integer input.
2. The final accumulated sum returned by `calculate_all` is inconsistent between runs due to a race condition in the concurrent execution.

Your objectives are:
1. Write a script or use an interactive Python session to fuzz/test the `process_number` function with integers between `-100000` and `100000`. Find the exact integer that causes the `ZeroDivisionError`. Write this single integer to `/home/user/crash_input.txt`.
2. Fix the code in `/home/user/calc_series.py`:
   - Catch the `ZeroDivisionError` (or fix the condition) in `process_number` so that it safely returns `0` when encountering that specific input.
   - Fix the concurrency race condition. You can use locks or refactor how the threading results are accumulated (e.g., summing mapped results), but it must still execute concurrently using `ThreadPoolExecutor`.
3. After fixing the code, modify the `__main__` block to execute `calculate_all(list(range(-100000, 100001)))`. 
4. Run the fixed script and write the final, correct integer sum to `/home/user/final_result.txt`.