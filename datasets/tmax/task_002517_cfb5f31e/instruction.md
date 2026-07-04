You are a developer fixing a hybrid multi-file Rust and C project that currently fails to build and test. The project is located in `/home/user/hybrid_image_filter`. 

The project uses a Rust `build.rs` to compile a C library, but the compilation fails because `build.rs` runs a C-based memory sanity check (`c_src/sanity_check.c`) that currently segfaults due to undefined behavior and memory leaks in the C library (`c_src/filter.c`).

Your objectives are:
1. **Memory Safety & UB Repair:** Fix the C code in `/home/user/hybrid_image_filter/c_src/filter.c`. The function `apply_filter(int* pixels, int width, int height)` has multiple memory safety issues:
   - It allocates incorrect memory sizes.
   - It contains an off-by-one heap buffer overflow.
   - It leaks memory before returning.
   Fix these issues so the sanity check passes without segmentation faults or memory leaks.

2. **Test Orchestration & Benchmarking:** Create a bash script at `/home/user/run_validation.sh` that does the following:
   - Navigates to `/home/user/hybrid_image_filter`.
   - Compiles the C sanity check program using AddressSanitizer (`gcc -fsanitize=address -g c_src/sanity_check.c c_src/filter.c -o sanity_check`).
   - Runs `./sanity_check` and captures the exit code.
   - Runs `cargo test` to ensure the Rust FFI bindings work correctly.
   - Runs the provided benchmark in `c_src/bench.c` by compiling it with `-O3` and executing it. The benchmark outputs the time taken in milliseconds.
   - Extracts the millisecond value from the benchmark output and writes it to `/home/user/benchmark_result.txt` strictly in the format: `BENCHMARK_MS=<value>`.

Ensure your bash script is executable (`chmod +x`). 
The `run_validation.sh` script should return an exit code of `0` if all tests and sanitizers pass, and `1` otherwise.