You are a support engineer tasked with debugging a critical mathematical diagnostic tool. 

A customer reported that their benchmarking tool, located at `/home/user/diagnostic`, hangs indefinitely on certain inputs and produces highly inaccurate results for others. The tool calculates a system damping coefficient mathematically equivalent to the exact value of `cos(x)` using a recursive Maclaurin (Taylor) series.

The customer provided the following details:
- When running `cargo run -- 15.0`, the tool produces an answer completely disjoint from reality.
- The recursive function occasionally hits the stack overflow fallback because of an infinite recursion bug.

Your objective is to fix the code in `/home/user/diagnostic/src/main.rs` by addressing three specific issues:
1. **Recursion / Loop Termination Fix**: The current termination condition is flawed because it expects an exact floating-point match. Change the base case so the recursion strictly terminates and returns `0.0` when the absolute value of `term` is strictly less than `1e-12`.
2. **Formula Correction**: The current implementation computes the next term using the wrong denominator, causing it to diverge from the `cos(x)` series. Correct the recursive formula so it mathematically matches the true Taylor series for cosine.
3. **Floating-point Precision Repair**: The program currently uses `f32`, which leads to catastrophic cancellation for larger inputs like `15.0`. Upgrade all mathematical logic, variables, constants, and function signatures in `main.rs` to use `f64`.

Once you have fixed the code:
1. Build the updated project using `cargo build`.
2. Run the program with the argument `15.0`.
3. Save the exact output (which should resemble `Result: <value>`) to `/home/user/result.txt`.