You are a performance engineer tasked with profiling and fixing a spectral analysis pipeline. The pipeline processes observational spectroscopy data, reshapes it, and computes bootstrap confidence intervals to estimate signal bounds. However, we've noticed that our results are not exactly reproducible between runs. The root cause is suspected to be non-deterministic floating-point reduction order in our vendored statistics library due to a naive parallel implementation.

Your goals are to fix the library, write a processing tool, and ensure the output is exactly reproducible.

1. **Fix the Vendored Package:**
   We vendor a library at `/app/fast_bootstrap-1.0` that computes bootstrap confidence intervals.
   - Attempting to compile it currently fails due to a broken `Makefile` (it has a typo in the compiler variable and is missing the `-fPIC` flag required to build a shared library). Fix the `Makefile`.
   - The library contains a non-deterministic floating-point accumulation in `bootstrap.cpp` (it uses an OpenMP parallel for loop with a floating-point reduction that causes minor round-off variations depending on thread timing). Modify `bootstrap.cpp` to make the sum accumulation strictly sequential and deterministic.
   - Build and install the library (you can keep the compiled `.so` and `.h` files in the package directory).

2. **Write the Analysis Tool:**
   Create a C++ program at `/home/user/analyzer.cpp` that uses this library.
   - **Command-line arguments:** `./analyzer <input.bin> <output.bin>`
   - **Input Format:** A raw binary file containing 32-bit floating-point numbers (little-endian). The data represents observational spectra. The number of frequency bins $M$ is fixed at **128**. The total number of floats in the file will be a multiple of 128. Let $N$ be the number of observations ($N = \text{total floats} / 128$).
   - **Data Reshaping:** Read the data. The input stores observation 0 (all 128 bins), then observation 1, etc.
   - **Processing:** For each frequency bin $i \in [0, 127]$, you must collect all $N$ values for that bin. Then, use the vendored library's function:
     `void compute_ci(const float* data, int n, int seed, float& mean, float& lower, float& upper);`
     Pass the $N$ values for bin $i$. Use a fixed random seed of `42 + i` for the $i$-th bin to ensure we get reproducible bootstrap sampling.
   - **Output Format:** Write exactly 128 records to `<output.bin>`, where each record consists of three 32-bit floats: `[mean, lower_bound, upper_bound]`.
   - **Convergence/Performance Note:** Ensure you compile your `analyzer.cpp` with `-O3` and link against the fixed `libfast_bootstrap.so`.

Ensure your final program `/home/user/analyzer` matches the expected deterministic output perfectly for any valid input file. We will test it against a reference oracle with randomly generated input arrays.