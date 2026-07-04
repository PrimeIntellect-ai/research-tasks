You are a bioinformatics analyst working on a statistical pipeline. We are evaluating the posterior distribution of a mutation rate parameter over a large set of genetic sequences using numerical integration. 

We have a Rust project located at `/home/user/bio_mcmc`. The project reads a dataset of sequence likelihoods (`/home/user/bio_mcmc/sequence_likelihoods.txt`), performs numerical integration using the trapezoidal rule, and compares the result against a reference. 

However, we are experiencing non-reproducible and inaccurate results. The previous developer used `f32` for the accumulation and an unordered parallel reduction (`rayon`) which causes floating-point reduction order issues and loss of precision.

Your task is to:
1. Modify `/home/user/bio_mcmc/src/main.rs` to fix the `calculate_integral` function.
2. Ensure the accumulation is deterministic and avoids `f32` precision loss by performing the summation sequentially using `f64` for the accumulator. 
3. The dataset contains pairs of `(x, y)` values. The numerical integration should compute the standard trapezoidal rule sum: `sum(0.5 * (y_{i} + y_{i+1}) * (x_{i+1} - x_{i}))` over the sorted input data. 
4. Run the Rust project and write the final computed integral (printed by the program) into a file named `/home/user/integral_result.txt`. The value should be printed as a standard float, rounded to 4 decimal places.

Do not change the input reading logic, just fix the computation and types in the integration step.