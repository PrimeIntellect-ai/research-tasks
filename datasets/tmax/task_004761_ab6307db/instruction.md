You are a performance and scientific computing engineer troubleshooting a Rust-based DNA sequence analysis tool. 

We have a custom Rust application in `/home/user/primer_opt` that optimizes primer design parameters (temperature, GC constraints) for a set of DNA sequences using a custom Gauss-Newton solver. Recently, the application has been crashing or returning `NaN`s during the optimization phase.

A previous engineer's profiling indicated that the failure occurs during the matrix factorization step of the optimization algorithm. Specifically, the Jacobian transpose times Jacobian matrix ($J^T J$) becomes near-singular for our latest target sequences, causing the standard linear solver to fail or lose numerical stability.

Your tasks are to:
1. Diagnose and fix the numerical instability in the Rust application located in `/home/user/primer_opt`. 
2. The fix must be mathematically sound: modify the Gauss-Newton step to become a Levenberg-Marquardt step (or Tikhonov regularization) by adding a damping factor of `1e-3` ($\lambda = 0.001$) to the diagonal of the $J^T J$ matrix before solving the linear system.
3. Once the code is fixed, build and run the application in release mode using the provided input file `/home/user/data/sequences.txt`.
4. The application, when running successfully, will output the optimized parameters to `/home/user/output/optimized_primers.json`. Ensure this file is generated.
5. In addition to fixing the Rust code, validate the analytical solution by writing a short bash or python script to parse `/home/user/output/optimized_primers.json` and calculate the average of the "final_score" values across all sequences. Save this single floating-point number (rounded to 3 decimal places) to `/home/user/output/average_score.txt`.

Constraints:
- Do not change the objective function or the Jacobian calculation, only the linear system solving step where the matrix inversion/factorization happens.
- You must use `nalgebra` as it is currently set up in the project.
- The output JSON file must have exactly the format the application natively produces.