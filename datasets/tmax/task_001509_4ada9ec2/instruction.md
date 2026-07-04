You are a performance engineer analyzing the execution time variability of a scientific computing workload before and after a recent optimization pass. 

You have two log files containing raw execution times (in milliseconds) for 5,000 independent mesh decomposition tasks:
1. `/home/user/baseline_perf.csv`
2. `/home/user/optimized_perf.csv`

To perform your statistical analysis directly in the terminal, you need to use GNU Datamash. However, the system does not have it installed, and you are in an offline environment. A source distribution of `datamash-1.8` has been vendored for you at `/app/datamash-1.8`. 

Your objectives are:
1. **Fix and Build Datamash**: The vendored `datamash-1.8` source has a deliberate perturbation in its build configuration that prevents it from compiling successfully. Identify the issue, fix it, compile, and install the tool locally so you can use it in your scripts.
2. **Bootstrap Confidence Intervals**: Write a Bash script `/home/user/analyze.sh` that uses your compiled `datamash` (or a combination of Bash, Awk, and Python) to generate a 95% bootstrap confidence interval (using 1,000 resamples) for the *difference in mean execution times* (Baseline Mean - Optimized Mean).
3. **Distribution Distance**: Compute the Wasserstein-1 distance between the full baseline distribution and the full optimized distribution to quantify the overall shift in the probability density.
4. **Report Output**: Your script `/home/user/analyze.sh` must output a JSON file to `/home/user/perf_report.json` exactly in this format:
```json
{
  "mean_diff_ci_lower": <float>,
  "mean_diff_ci_upper": <float>,
  "wasserstein_distance": <float>
}
```

Constraints:
- You must rely on the offline vendored package at `/app/datamash-1.8`. Do not attempt to download packages from the internet.
- Ensure your Bash script computes the values correctly and outputs the JSON file. The automated verifier will parse this JSON and check your calculated metrics against the reference values within a strict tolerance.