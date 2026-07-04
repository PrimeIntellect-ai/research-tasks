You are an AI assistant helping a data researcher validate the reproducibility of their mathematical models.

The researcher has output files from two different pipeline runs on the same dataset, located at `/home/user/run1.txt` and `/home/user/run2.txt`. Each file contains exactly 100 floating-point numbers, one per line, representing model predictions.

To test the pipeline's reproducibility and validate the output, you must determine if there is a statistically significant drift between the two runs.

Your task is to write a Rust program that calculates the paired differences between the two runs (Run 1 minus Run 2 for each line), and computes the mean difference along with its 95% confidence interval.

**Requirements:**
1. Create a Rust Cargo project named `repro_check` in `/home/user/`.
2. Write the Rust code to read the two files, compute the paired differences $d_i = \text{run1}_i - \text{run2}_i$.
3. Calculate the sample mean of the differences ($\bar{d}$).
4. Calculate the sample standard deviation of the differences ($s_d$). Use $N-1$ (Bessel's correction) for the sample variance.
5. Compute the 95% Confidence Interval for the mean difference. **Use a Z-value of exactly 1.96** for the margin of error calculation.
6. Run the Rust program.
7. The program must append exactly one line to `/home/user/validation_log.txt` with the following format (rounding values to exactly 4 decimal places):
`MEAN_DIFF: <mean>, CI_LOWER: <lower_bound>, CI_UPPER: <upper_bound>`

Example output format:
`MEAN_DIFF: -0.2000, CI_LOWER: -0.2591, CI_UPPER: -0.1409`

Make sure your Rust code handles the basic math and file I/O operations strictly according to the formulas for paired sample confidence intervals.