You are a build engineer managing a polyglot Python package called `math_accelerator` that provides high-performance numerical algorithms. The project resides in `/home/user/math_accelerator`. 

Recently, a junior developer attempted to restructure the project but broke the build configuration and left a pure-Python fallback implementation incomplete. 

Your task is to fix the package, implement the missing logic, and benchmark the results.

Here is what you need to do:

1. **Fix the Build Orchestration:** 
   The `setup.py` file in `/home/user/math_accelerator` is incomplete. The package contains a C extension source file at `/home/user/math_accelerator/src/trib_c.c` that implements the "Tribonacci" sequence. Fix `setup.py` so that when you run `pip install -e .` inside the directory, it successfully compiles the C extension and exposes it as the module `math_accelerator.trib_c`.

2. **Implement the Numerical Algorithm Fallback:**
   The pure-Python fallback file at `/home/user/math_accelerator/math_accelerator/trib_py.py` has an empty `tribonacci(n)` function. Implement it. The Tribonacci sequence is defined as:
   - T(0) = 0
   - T(1) = 1
   - T(2) = 1
   - T(n) = T(n-1) + T(n-2) + T(n-3) for n >= 3
   Your implementation must return the correct integer for any n >= 0.

3. **Performance Benchmarking:**
   Create a benchmarking script at `/home/user/benchmark.py`. This script must:
   - Import both the C extension (`math_accelerator.trib_c.tribonacci`) and the pure-Python fallback (`math_accelerator.trib_py.tribonacci`).
   - Verify that both functions return the exact same value for `n = 25`.
   - Use the `timeit` module to measure the execution time of running `tribonacci(25)` exactly 100 times for *each* implementation.
   - Output the results to a JSON file at `/home/user/benchmark_results.json` strictly matching this format:
     ```json
     {
         "value_25": <the exact integer value of Tribonacci(25)>,
         "c_faster_than_py": <boolean indicating if the C extension took less time than the Python implementation>
     }
     ```

Ensure all files are saved and properly formatted before completing the task.