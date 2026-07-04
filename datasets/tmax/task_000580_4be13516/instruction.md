You are an AI assistant acting as a bioinformatics analyst. 

You have been provided with a dataset of DNA sequence read lengths from an experimental sequencing run. The data is located at `/home/user/seq_lengths.txt`. The file contains sequence lengths, but the data is poorly formatted: multiple comma-separated lengths appear on each line.

Your task:
1. Reshape the observational data into a flat list or 1D array of sequence lengths.
2. Using Python and `scipy.stats`, fit two probability distributions to this empirical data: a Normal (`norm`) distribution and an Exponential (`expon`) distribution.
3. Compare the statistical hypothesis that the data follows the fitted Normal distribution versus the fitted Exponential distribution by performing a Kolmogorov-Smirnov (KS) test for both.
4. Determine which distribution is a better fit (has the higher p-value from the KS test).
5. Output the result to `/home/user/best_fit.log`. The file should contain exactly one line with the name of the best-fitting distribution (either `normal` or `exponential` in all lowercase) and its KS test p-value rounded to 4 decimal places, separated by a comma (e.g., `exponential,0.1234`).

Note: 
- You should use `scipy.stats.norm.fit` and `scipy.stats.expon.fit` to get the distribution parameters.
- Pass these fitted parameters to `scipy.stats.kstest`.