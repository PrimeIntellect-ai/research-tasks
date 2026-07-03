You are an assistant helping a systems researcher evaluate a new network queueing algorithm. The researcher has run simulations of the old system and the new system, recording the packet latencies.

Your task is to write a Bash script that orchestrates the comparison of these two datasets, fits basic distribution parameters, calculates a bootstrap confidence interval, and draws a statistical conclusion.

**Input Files:**
Two text files, each containing one latency measurement (float) per line.
1. `/home/user/ref_latency.txt` (The reference/old algorithm)
2. `/home/user/test_latency.txt` (The test/new algorithm)

**Deliverable:**
Create a Bash script at `/home/user/compare_models.sh`. 
The script must take two positional arguments (the reference file and the test file) and print a specific report to standard output. While the script itself must be Bash, you may use inline Python (`python3 -c "..."` or a heredoc) within the script to perform the mathematical operations.

When run via:
`bash /home/user/compare_models.sh /home/user/ref_latency.txt /home/user/test_latency.txt > /home/user/report.txt`

The script must produce exactly 4 lines of output in the following format (round all floats to 2 decimal places):
```
Ref: Mean=XX.XX, Std=XX.XX
Test: Mean=XX.XX, Std=XX.XX
CI: [XX.XX, XX.XX]
Conclusion: [RESULT]
```

**Statistical Requirements:**
1. **Density/Distribution parameters:** Calculate the empirical mean and standard deviation (using the sample standard deviation with degrees of freedom = 1) for both datasets.
2. **Bootstrap Confidence Interval:** Calculate a 95% bootstrap confidence interval for the *difference in means* (`Test Mean - Ref Mean`). 
    * You must use exactly 5000 bootstrap iterations.
    * In each iteration, resample with replacement from the Test dataset to find a bootstrap test mean, and resample with replacement from the Ref dataset to find a bootstrap ref mean. Subtract the ref mean from the test mean.
    * Use the 2.5th and 97.5th percentiles of these 5000 differences for the bounds.
    * **Crucial:** To ensure verifiability, you must set `numpy.random.seed(42)` immediately before your bootstrap loop if using Python.
3. **Conclusion:** 
    * If the upper bound of the CI is less than `0.00`, output `IMPROVED` (latency significantly decreased).
    * If the lower bound of the CI is greater than `0.00`, output `DEGRADED` (latency significantly increased).
    * Otherwise, output `UNCHANGED`.

After writing the script, execute it as requested to generate `/home/user/report.txt`.