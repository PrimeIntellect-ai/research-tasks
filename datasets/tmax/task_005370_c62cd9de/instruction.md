You are a performance engineer tasked with debugging and optimizing a Python application for scientific computing. 

You have been given access to a project in the `/home/user/app` directory containing two files:
1. `/home/user/app/computation.py`: Contains math routines.
2. `/home/user/app/env.sh`: An environment configuration script sourced before running the application.

Currently, there are three major issues:
1. **Numerical Instability**: The function `compute_log_sum_exp(x)` in `computation.py` suffers from floating-point overflow when given large inputs (e.g., `x = [1000.0, 1000.0]`), returning `inf`. Diagnose and repair this floating-point precision issue using the standard stable log-sum-exp trick (do not use `scipy.special.logsumexp`, implement it manually using NumPy).
2. **Environment Misconfiguration**: The function `expensive_computation()` in `computation.py` performs a large matrix multiplication. When run after sourcing `env.sh`, it is unacceptably slow because the environment is misconfigured to throttle multi-threading. Repair `/home/user/app/env.sh` by changing all thread-limiting variables to allow exactly `4` threads. 
3. **Missing Test Coverage**: There are no tests to prevent regressions.

Your objectives:
1. Fix the numerical instability in `compute_log_sum_exp` within `/home/user/app/computation.py`.
2. Repair the environment misconfiguration in `/home/user/app/env.sh` by changing all the thread limits to `4`.
3. Construct a regression test file at `/home/user/app/test_computation.py` using `pytest`. It must include:
   - `test_log_sum_exp()`: Asserts that `compute_log_sum_exp(np.array([1000.0, 1000.0]))` evaluates correctly (approx `1000.6931471805599`). Use `np.isclose`.
   - `test_log_sum_exp_large()`: Asserts that `compute_log_sum_exp(np.array([5000.0, 5001.0]))` evaluates correctly without overflowing.
4. Run your tests to verify they pass, and save the output of the test run to `/home/user/app/test_results.log`. (e.g., `pytest test_computation.py > test_results.log`)

Ensure all your code is fully functional, properly imports necessary libraries (`numpy`), and correctly implements the numerical fixes.