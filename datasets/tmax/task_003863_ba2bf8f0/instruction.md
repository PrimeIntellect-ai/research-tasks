You are a data scientist tasked with analyzing a large set of empirical distributions. 

You have been provided with an HDF5 file located at `/home/user/data.h5`. This file contains a single dataset named `empirical_data` with shape `(200, 1000)`. Each of the 200 rows represents an independent sample of 1000 observations.

Your objective is to:
1. Write a Python script (`/home/user/fit_and_compare.py`) that reads the HDF5 file.
2. For each row, fit a Normal distribution to the data (find the Maximum Likelihood Estimate for the mean and standard deviation).
3. Compute the Wasserstein distance between the empirical data in that row and the fitted Normal distribution. To do this deterministically, compare the empirical row data against 1000 evenly spaced percentiles of the fitted Normal distribution (using `scipy.stats.norm.ppf` with probabilities `np.linspace(0.001, 0.999, 1000)`).
4. You **must** process the rows in parallel using Python's `multiprocessing` library (use 4 worker processes).
5. Save the resulting 200 Wasserstein distances to `/home/user/distances.csv`, with one value per line.
6. Finally, write an R script (`/home/user/test_hypothesis.R`) that reads `/home/user/distances.csv` and performs a one-sample t-test to test the null hypothesis that the true mean of the Wasserstein distances is equal to 0.1 (against the two-sided alternative). Save the exact p-value (just the numeric value) to a file named `/home/user/pvalue.txt`.

Run both scripts to generate the required output files (`distances.csv` and `pvalue.txt`).