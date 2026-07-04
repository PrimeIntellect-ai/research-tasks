I need you to help me optimize and fix a C-based numerical integrator used for solving non-linear equations in our physics simulations. 

Currently, we have a reference implementation provided as a stripped binary at `/app/integrator_oracle`. This binary reliably finds the root of a specific non-linear equation $f(x) = \int_0^x g(t) dt - C = 0$ within a high precision, but we don't have its source. 

We also have our own C implementation at `/home/user/integrator.c` which currently suffers from two issues:
1. It is extremely slow because it doesn't utilize parallel computing.
2. It diverges for some inputs due to a naive step-size adaptation in the integration step.

Your task is to:
1. Analyze the oracle binary's behavior to understand the expected output format and accuracy. The oracle takes two arguments: an initial guess and a target constant $C$.
2. Modify `/home/user/integrator.c` to fix the numerical divergence (implement a robust root-finding algorithm combined with adaptive Simpson's rule or Runge-Kutta).
3. Parallelize the integration loop using OpenMP (`#pragma omp parallel`).
4. Create a bash script `/home/user/test_regression.sh` that compiles your C code (with `-O3 -fopenmp`), runs both the oracle and your compiled program over 100 random inputs, and computes a bootstrap 95% confidence interval for the average speedup of your program compared to the oracle.
5. Save the final compiled optimized executable at `/home/user/fast_integrator`.

Your optimized version must achieve an output accuracy within 1e-6 of the oracle's output for any given input, and must achieve a speedup of at least 2.0x on average over the oracle (which is single-threaded). The script `/home/user/test_regression.sh` should output a single line with the lower bound of the speedup confidence interval.