You are a performance engineer tasked with optimizing a scientific application that generates synthetic spectroscopy signals. The current implementation evaluates the signal over a 1D mesh but is extremely slow due to inefficient sequential processing.

Your task is to optimize the code and perform a statistical regression test to ensure correctness.

1. **Optimize the Simulation**: 
   The script `/home/user/simulate.py` takes too long to run. Modify it to implement a domain decomposition approach. You must split the input array `x` into 4 equal-sized chunks and process them in parallel using Python's `multiprocessing.Pool`. 
   - Keep the mathematical operations inside `compute_spectrum` mathematically identical.
   - The optimized script must save its output to `/home/user/output_fast.npy` instead of `output.npy`.

2. **Regression Testing & Statistical Verification**:
   To guarantee that your parallelization did not introduce any artifacts or ordering issues, you need to write a regression test script at `/home/user/test_regression.py`.
   - This script must load the pre-computed ground truth from `/home/user/reference.npy` and your new output from `/home/user/output_fast.npy`.
   - Use `scipy.stats.ks_2samp` to perform a two-sample Kolmogorov-Smirnov test to compare the distributions of the two signal arrays.
   - The script must save a JSON report to `/home/user/report.json` with the exact structure:
     `{"p_value": <float>, "passed": <bool>}`
     where `"passed"` is `true` if `"p_value"` > 0.99, and `false` otherwise.

3. **Execution**:
   Run your optimized `/home/user/simulate.py` and then run `/home/user/test_regression.py` to generate the final `report.json`.