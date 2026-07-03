You are an operations engineer triaging a critical incident. The nightly risk-scoring batch job is failing in production. 

The batch job consists of a Bash orchestration script that calls a compiled C helper to perform mathematical calculations (an iterative root-finding algorithm to find system equilibrium). The job is located in `/home/user/risk_job`.

Currently, the job is failing for three distinct reasons:
1. **Build Failure:** The C helper fails to compile due to linker errors when running `make`.
2. **Assertion Failure:** The orchestration script has an assertion checking the iteration tolerance, but it is throwing a syntax error.
3. **Convergence Failure:** Even when the script runs, the iterative math sequence hits the maximum iteration limit (20) without converging, due to a precision loss issue in the Bash math pipeline.

Your task is to:
1. Fix the `Makefile` in `/home/user/risk_job` so the C code compiles correctly.
2. Fix the assertion bug in `/home/user/risk_job/run_job.sh`.
3. Fix the convergence issue in `/home/user/risk_job/run_job.sh` so the algorithm converges within the 20-iteration limit.

Once you have fixed the issues, run `/home/user/risk_job/run_job.sh`. If successful, the script is designed to output a file at `/home/user/risk_job/success.log` containing the final converged value.

Do not change the initial starting value (`X=5.0`), the tolerance (`0.0001`), the math formula in the C code, or the maximum iteration limit. You may only fix the build step, the bash comparison logic, and the bash math precision.