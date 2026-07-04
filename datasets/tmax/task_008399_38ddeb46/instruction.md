You are a performance engineer working on optimizing a scientific simulation code. The current pure-Python implementation is accurate but too slow for large-scale production runs. Your team has provided a highly optimized C function for the core computational kernel, but it only processes 1D data arrays.

Your objective is to compile the C kernel, write a Python wrapper that uses mesh domain decomposition (splitting the array into chunks) and multiprocessing to process the data in parallel, verify your new implementation against the slow baseline using regression testing, and profile the new code.

All work should be done in `/home/user/sim_project`.

Here are your specific tasks:

1. **Compile the Scientific C Code:**
   Inside `/home/user/sim_project`, you will find `kernel.c`. Compile this into a shared library named `libkernel.so` using GCC. Ensure it is compiled with position-independent code (PIC) and standard shared library flags.

2. **Implement Parallel Domain Decomposition:**
   Create a Python script at `/home/user/sim_project/fast_solver.py`. This script must:
   - Contain a function `parallel_solve(data: np.ndarray, num_workers: int) -> np.ndarray`.
   - The function should accept a 1D float64 numpy array.
   - It must split the array into `num_workers` equal-sized continuous chunks (you can assume the length of `data` will always be perfectly divisible by `num_workers`).
   - Use Python's `multiprocessing.Pool` (or `concurrent.futures.ProcessPoolExecutor`) to process each chunk in parallel.
   - For each chunk, use `ctypes` to invoke the `process_chunk` function from `libkernel.so`. The C function signature is `void process_chunk(double* input, double* output, int size)`.
   - Combine the processed chunks back into a single 1D numpy array and return it.

3. **Run Regression Tests:**
   A regression test script `/home/user/sim_project/test_regression.py` is provided. It compares your `fast_solver.parallel_solve` against the slow pure-Python baseline. Run this test using `pytest` to ensure your parallel implementation is numerically identical to the baseline. The tests must pass.

4. **Profile the Execution:**
   Create a script `/home/user/sim_project/run_profile.py` that:
   - Generates a random 1D numpy array of size `10,000,000` (float64) using `numpy.random.rand`.
   - Calls your `parallel_solve(data, num_workers=4)`.
   Run this script using `cProfile` and output the profiling statistics to a file named `/home/user/sim_project/profile_data.prof` (e.g., using `python -m cProfile -o ...`).

Ensure all scripts are executable and the final `.prof` file is successfully generated.