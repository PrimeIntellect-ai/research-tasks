You are a developer tasked with debugging a failing build for a C-based numerical statistics engine. 

The project is located in `/home/user/stats_engine`. 

Currently, the project fails to build, and even when forced, its test suite fails due to a severe numerical instability. Your task is to diagnose the environment issue, fix the numerical bug, and provide a minimized test case.

Here are your specific objectives:

1. **Fix the Build Environment:** The `Makefile` in `/home/user/stats_engine` is misconfigured. When you run `make`, it fails to build the `run_tests` executable because it cannot resolve basic math symbols. Diagnose and fix the Makefile so that `make` and `make test` run successfully.

2. **Diagnose and Fix Numerical Instability:** The function `calculate_variance` in `src/stats.c` uses a naive single-pass formula to calculate the sample variance: `(sum(x^2) - sum(x)^2 / n) / (n - 1)`. When the input data has a very large mean but a small variance (e.g., `[1e9, 1e9 + 1, 1e9 + 2]`), this formula suffers from catastrophic cancellation, resulting in `0.0` or even negative numbers.
   * Modify `src/stats.c` to use a numerically stable algorithm for calculating sample variance (e.g., a two-pass algorithm calculating the mean first, then sum of squared differences, or Welford's algorithm).
   * Ensure it returns the correct sample variance.

3. **Create a Minimized Test:** 
   * Write a minimized C program in `/home/user/stats_engine/minimized_test.c` that demonstrates this exact failure. 
   * The program should initialize an array with exactly three `double` values: `1000000000.0`, `1000000001.0`, and `1000000002.0`.
   * It should call `calculate_variance` (include `stats.h`), and if the variance is strictly equal to `1.0`, it should return `0` (success). Otherwise, it should return `1` (failure).

4. **Verify and Finalize:**
   * Run `make test` to ensure the official test suite now passes.
   * Compile your minimized test manually to ensure it works with your fixed `stats.c`: `gcc -I./src -o minimized_test minimized_test.c src/stats.c -lm`
   * Once `make test` succeeds and `minimized_test` compiles and exits with code 0, write the exact word `SUCCESS` to `/home/user/stats_engine/status.txt`.

Do not change the function signatures in `src/stats.h`. Ensure all paths are absolute or correctly relative to `/home/user/stats_engine`.