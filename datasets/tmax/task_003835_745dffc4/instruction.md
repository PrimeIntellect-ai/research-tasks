You are a performance engineer tasked with validating a new, highly optimized simulation function against an older, slower baseline. You have been given a script `/home/user/simulate.py` containing two functions: `simulate_v1` (the trusted baseline) and `simulate_v2` (the new vectorized version). 

Unfortunately, `simulate_v2` seems to produce results that are statistically different from `simulate_v1`, suggesting a subtle bug in its implementation.

Your tasks are:
1. Analyze both functions in `/home/user/simulate.py` and identify the bug in `simulate_v2` that causes the distribution of its outputs to differ from `simulate_v1`. Fix the bug in `/home/user/simulate.py` so that `simulate_v2` produces a statistically indistinguishable distribution.
2. Create a Python script `/home/user/compare.py` that compares the outputs of `simulate_v1(10000, seed=42)` and the *fixed* `simulate_v2(10000, seed=42)`.
3. In `/home/user/compare.py`, compute the following metrics using `scipy.stats`:
   - The 1D Wasserstein distance between the two datasets.
   - The p-value from the 2-sample Kolmogorov-Smirnov (KS) test between the two datasets.
4. `/home/user/compare.py` must save these results to a JSON file at `/home/user/comparison.json` with the exact following structure:
```json
{
  "wasserstein_distance": <float>,
  "ks_pvalue": <float>
}
```
5. Run your comparison script to generate the final `/home/user/comparison.json`.

Ensure your fix to `simulate_v2` correctly aligns the probability distributions (both are simulating a 100-step 1D random walk). You may install any necessary packages (like `numpy`, `scipy`) using `pip`.