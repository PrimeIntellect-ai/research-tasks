You are a technical support engineer diagnosing a customer's mathematical simulation software. The customer provided a minimal reproducible example of their Rust project located at `/home/user/sim_solver`. They are experiencing two major issues:

1. **Build/Environment Failure**: The project currently fails to compile and link. The customer mentioned they recently copied some workspace configurations from an old C++ integration project, which might be polluting the build environment. 
2. **Convergence Failure**: Even when the customer temporarily bypassed the build error in the past, the mathematical solver (a Newton-Raphson implementation in `src/main.rs`) failed to converge. It oscillates infinitely and prints "Failed to converge" instead of finding the root of the equation $f(x) = x^3 - 2x + 2$.

Your task is to collect diagnostics and fix the minimal example:
1. Identify and remove the misconfigured environment or compiler flags causing the linker error.
2. Read `src/main.rs` and diagnose the numerical oscillation. To fix the numerical instability and allow the solver to converge, change the initial guess variable `x` in `src/main.rs` from its current value to `-2.0`.
3. Verify the fix by successfully compiling and running the project.
4. Save the standard output of the successful `cargo run` command to `/home/user/diagnostics.log`. 

The log file must contain the exact single line of output from the program upon successful convergence (e.g., `Converged root: <value>`).