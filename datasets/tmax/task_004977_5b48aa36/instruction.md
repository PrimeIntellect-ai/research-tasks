I'm debugging a failing CI build for my numerical integration Rust library. The container's build log indicates that our tests are failing, but I haven't been able to figure out why.

The project is located at `/home/user/num_calc`.
The CI build logs are dumped in `/home/user/ci_build.log`.

The library exposes a `left_riemann_sum` function that calculates the integral of `f(x) = x^2` over a given range. However, the test `test_integral_precision` is failing. I suspect there are two issues in `src/lib.rs`:
1. A precision loss issue accumulating floating-point values.
2. An off-by-one boundary condition error in the loop.

Your task is to:
1. Inspect the log and the code in `/home/user/num_calc/src/lib.rs`.
2. Fix the precision loss and the off-by-one error in the `left_riemann_sum` function so that `cargo test` passes cleanly. Do not change the function signature or the test assertions.
3. Extract the core function into a minimal reproducible example. Create a standalone Rust script at `/home/user/mre.rs` that includes the fixed function, and a `main` function that calls `left_riemann_sum(0.0, 100.0, 1000)` and prints the output to stdout.

Ensure that running `cargo test` in `/home/user/num_calc` executes successfully and that `rustc /home/user/mre.rs && ./mre` correctly prints the output.