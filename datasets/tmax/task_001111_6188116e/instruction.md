You are a performance engineer analyzing the efficiency of a new primer matching algorithm used in a bioinformatics pipeline. Your goal is to parse raw observational profiling data, compute alignment scores, and statistically verify if the new algorithm ("AlgoB") is significantly faster than the baseline ("AlgoA").

You must complete this task using **Rust** as your primary programming language.

**Phase 1: Environment & Setup**
1. Initialize a new Rust binary project at `/home/user/profiler`.
2. A raw observational data file is located at `/home/user/raw_profiling.txt`. 

**Phase 2: Observational Data Reshaping & Primer Alignment**
The `raw_profiling.txt` file uses a pipe-separated format: `RunID|Algorithm|TargetSequence|PrimerSequence|ExecutionTimeNs`
Write a Rust program that parses this file and calculates a "Primer Match Score" for each row. 
* The matching rule: The score is the number of characters in the `PrimerSequence` that exactly match the corresponding character in the `TargetSequence` at the same index, starting from index 0. (Assume `TargetSequence` is always at least as long as `PrimerSequence`).
* Reshape and save this data into a new CSV file at `/home/user/reshaped_data.csv` with the exact header: `run_id,algorithm,match_score,time_ns`.

**Phase 3: Statistical Hypothesis Comparison**
Using your Rust program, extract the execution times (`time_ns`) for `AlgoA` and `AlgoB`. 
1. Perform a **Welch's t-test** (two-tailed) comparing the execution times of `AlgoA` vs `AlgoB`. 
2. You must calculate the sample means and sample variances (using N-1 for variance). 
3. Calculate the T-statistic and the degrees of freedom ($\nu$).
4. Calculate the two-tailed P-value. You may use external crates like `statrs` in your `Cargo.toml`.
5. Determine if the null hypothesis (that the mean execution times are equal) is rejected at a significance level of $\alpha = 0.05$.

**Phase 4: Reporting**
Output your final results to a JSON file located exactly at `/home/user/profiling_report.json` with the following schema:
```json
{
  "algo_a_mean": 1234.5,
  "algo_b_mean": 1100.2,
  "t_statistic": 4.567,
  "degrees_of_freedom": 45.123,
  "p_value": 0.00012,
  "significant_at_05": true
}
```
*Note: Float values in your JSON should be rounded to at least 4 decimal places, or left unrounded. The automated tests will verify them within a tight tolerance (1e-3).*

Ensure your Rust project compiles and runs cleanly, producing both `/home/user/reshaped_data.csv` and `/home/user/profiling_report.json`.