You are acting as a data scientist analyzing the posterior distribution of a spatial model. You have a set of MCMC samples representing the global mean temperature parameter of the model, and you need to calculate the bootstrap confidence intervals for this parameter to validate against historical regression data.

Your task:
1. Write a Go program at `/home/user/bootstrap_mcmc.go` that reads `/home/user/mcmc_samples.csv`. This file contains one floating-point number per line representing individual MCMC draws.
2. The Go program must compute:
   - The exact mean of the original samples.
   - The 95% bootstrap confidence interval of the mean using the percentile method (2.5th and 97.5th percentiles).
3. For the bootstrap process:
   - Use exactly 10,000 resampling iterations (with replacement).
   - Use Go's `math/rand` with a fixed seed of `42` (`rand.New(rand.NewSource(42))`) for reproducibility.
   - For calculating the percentiles after sorting the 10,000 resampled means, use the exact indices `250` (for 2.5%) and `9749` (for 97.5%).
4. The program must output the results to `/home/user/posterior_summary.json` in the following exact format:
   ```json
   {
     "mean": 2.503,
     "ci_lower": 2.102,
     "ci_upper": 2.855
   }
   ```
5. Compile and run your Go program to generate the JSON file.

Note: You must implement the bootstrap logic yourself in Go, relying only on standard library packages (`os`, `encoding/csv`, `encoding/json`, `math`, `math/rand`, `sort`, `strconv`, etc.).