You are a data scientist fitting a physical model. Part of the model's parameter estimation requires evaluating a sensitivity integral that behaves like a near-singular input, causing standard uniform-mesh numerical integration to fail or produce highly inaccurate results. 

Your objective is to fix a failing regression test in a Rust project by implementing domain decomposition and mesh refinement, and then validating the numerical result against the exact analytical solution.

**Background**
The integral in question evaluates the function:
`f(x) = 1.0 / sqrt(x^2 + alpha^2)`
over the domain `[-1.0, 1.0]`, where `alpha = 1e-4`.

Due to the sharp peak at `x = 0`, a uniform mesh severely underestimates the integral. The analytical solution for this definite integral over `[-1.0, 1.0]` is:
`Exact = 2.0 * arsinh(1.0 / alpha)`

**Instructions**
1. Initialize a new Rust executable project at `/home/user/model_fit` (using `cargo new`).
2. Write a Rust program in `/home/user/model_fit/src/main.rs` that calculates this integral using the **Trapezoidal Rule**.
3. To handle the near-singular peak, implement **domain decomposition**. Break the domain `[-1.0, 1.0]` into three sub-domains:
   - Left: `[-1.0, -0.01]` using 100 evenly spaced points (99 intervals).
   - Center: `[-0.01, 0.01]` using 1000 evenly spaced points (999 intervals).
   - Right: `[0.01, 1.0]` using 100 evenly spaced points (99 intervals).
4. Compute the numerical integral by summing the results of the Trapezoidal rule applied to these three sub-domains.
5. Compute the exact analytical solution in your Rust code.
6. Calculate the absolute error between the numerical and analytical solutions.
7. The program must output the results to a JSON file at `/home/user/integration_log.json` with exactly the following structure:
   ```json
   {
     "analytical": 19.806975883653198,
     "numerical": 19.806...,
     "error": 0.000...
   }
   ```
   *(Note: The analytical value above is an approximation; compute it precisely in your code using `f64`.)*

**Success Criteria**
- The project must compile successfully with `cargo build`.
- The program must generate the `/home/user/integration_log.json` file.
- The absolute error must be strictly less than `1e-4`.
- The mesh decomposition must precisely follow the point counts requested.