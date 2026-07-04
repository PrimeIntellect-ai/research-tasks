You are a data scientist preparing a reproducible computation pipeline for fitting models to Raman spectroscopy signals. To handle millions of spectra efficiently, you are writing the preprocessing steps in Rust.

Your preprocessing pipeline requires two steps:
1. Signal smoothing using a 3-point moving average.
2. Baseline correction (subtracting the minimum value of the smoothed signal from all data points).

You have been provided with a local, vendored Rust library located at `/app/spectro_filter`. This library is supposed to perform the 3-point moving average. However, the author warned you that it occasionally crashes during numerical stability testing due to an indexing bug at the boundaries of the array. 

Your tasks are:

1. **Fix the vendored library:**
   Inspect `/app/spectro_filter/src/lib.rs`. Fix the logic so that for an input array `data`, the first and last elements remain completely unchanged, and every middle element `i` is replaced by the arithmetic mean of `data[i-1]`, `data[i]`, and `data[i+1]`. Ensure it does not panic (e.g., "index out of bounds").

2. **Implement the CLI processor:**
   Create a new Rust binary project at `/home/user/spectro_cli` that depends on your fixed local `/app/spectro_filter` library.
   Write a program that:
   - Reads a single line of space-separated floating-point numbers from standard input (`stdin`).
   - If the input has fewer than 3 elements, it should print them out unmodified, but formatted to 4 decimal places.
   - Otherwise, applies the `apply_filter` function from `spectro_filter`.
   - Performs baseline correction on the smoothed signal by finding its minimum value and subtracting that minimum from every element.
   - Prints the final processed elements to standard output (`stdout`), separated by a single space, with each number formatted to exactly 4 decimal places (e.g., `0.0000 1.2345 0.5000`).

3. **Build the CLI:**
   Compile your CLI tool in release mode so the executable is located precisely at `/home/user/spectro_cli/target/release/spectro_cli`.

Constraints:
- You must not use any external crates downloaded from the internet; rely only on the standard library and the local `/app/spectro_filter` crate.
- Ensure the executable consumes `stdin` and writes to `stdout` directly.