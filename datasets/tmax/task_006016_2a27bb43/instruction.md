You are a bioinformatics analyst studying the accumulation of mutations in a rapidly evolving viral strain. You have collected sequence data over several discrete viral generations and counted the average number of novel mutations. You suspect the mutations are accumulating exponentially due to a cascading error-catastrophe (divergence), resembling a runaway numerical integrator.

You have a dataset located at `/home/user/mutations.tsv` with two columns: `Generation` (X) and `Mutations` (Y).

Your task is to write a Bash script, `/home/user/analyze_mutations.sh`, that performs the following statistical and mathematical analyses:

1. **Curve Fitting:** Fit the dataset to an exponential model: $Y = A \cdot e^{B \cdot X}$. Calculate the base growth rate `B` using Ordinary Least Least Squares (OLS) linear regression on the natural logarithm of `Y` ($\ln(Y)$).
2. **Bootstrap Confidence Intervals:** The script must use a Bash loop to perform 1000 bootstrap resamples of the dataset (resampling rows with replacement). For each resample, calculate the growth rate `B`. Find the 95% Confidence Interval for `B` by extracting the 2.5th percentile and 97.5th percentile of the bootstrapped `B` values (i.e., the 25th and 975th values when sorted).
3. **Divergence Testing:** Using the base `A` and `B` values calculated from the original full dataset, calculate the "Divergence Generation"—the smallest integer generation $X$ where the predicted number of mutations $Y$ strictly exceeds $100,000$.

**Constraints:**
- The primary orchestration and bootstrapping loop **must** be written in Bash (in `/home/user/analyze_mutations.sh`), though you may use inline `awk`, `bc`, or short inline `python3` snippets within the loop to perform the OLS calculations.
- You must set a fixed random seed if you use tools like `shuf`, `awk` or `python` for resampling so that your output is completely deterministic. Use the seed `42` for whatever PRNG you use for bootstrapping.

**Output:**
Your script must write the final results to `/home/user/report.txt` in exactly this format (rounded to 4 decimal places for floats):
```
Base Rate B: 0.1234
Bootstrap 2.5%: 0.1100
Bootstrap 97.5%: 0.1350
Divergence Gen: 45
```

Write the script, run it to generate the report, and ensure `/home/user/report.txt` contains the correct values.