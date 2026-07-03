You are a support engineer investigating a bug in a Rust-based physics simulation microservice. Customers are reporting intermittent crashes with the error "Numerical instability detected". 

We have extracted a minimal reproducible project in `/home/user/sim_tracker`. 

Your goals are:
1. **Fix compilation issues:** The diagnostic wrapper in `src/main.rs` currently fails to compile due to a minor formatting/type error. Fix it so you can run the CLI via `cargo run -- <seed>`.
2. **Reproduce the intermittent failure:** The instability only happens for certain random seeds. Write a diagnostic script to run the simulation with seeds from `1` to `100`. Find the **first** seed (numerically lowest) that causes the program to panic or return the numerical instability error.
3. **Capture diagnostics:** 
   - Write the failing seed to a file named `/home/user/failing_seed.txt`.
   - Save the exact standard error (stderr) output of that failing run to `/home/user/error_trace.log`.
4. **Fix the root cause:** The instability is caused by precision loss in the core loop in `src/lib.rs` (accumulating small values into an `f32`). Fix the code in `src/lib.rs` to use `f64` for the `state`, `step`, and `perturbation` calculations to eliminate the precision loss. 

When you are done, I should be able to run `cargo run -- <failing_seed>` successfully without it crashing.