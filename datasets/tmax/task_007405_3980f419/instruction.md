You are a bioinformatics analyst evaluating the sequencing quality of two different runs. You have been provided with two CSV files containing Phred quality scores: `/home/user/run1_scores.csv` and `/home/user/run2_scores.csv`. In these files, each row represents a read and each column represents a base position.

Your task is to analyze the difference in overall quality score distributions between the two runs. Please write and execute a Python script to do the following:

1. Read both CSV files and reshape the data by flattening all scores into two 1D arrays (one for run 1 and one for run 2).
2. Calculate the exact 1D Wasserstein distance between the two flattened score distributions (using `scipy.stats.wasserstein_distance`).
3. Compute a 95% bootstrap confidence interval for this distance. To do this, perform 1000 bootstrap iterations. In each iteration, independently sample with replacement from the flattened run 1 array and the flattened run 2 array (keeping the sample sizes equal to their respective original flattened array sizes), and compute the Wasserstein distance between the two resampled arrays.
4. Calculate the 2.5th and 97.5th percentiles of the 1000 bootstrapped distances to form the confidence interval.
5. **Crucial for reproducibility:** Set the random seed by calling `import numpy as np; np.random.seed(42)` exactly once, immediately before your bootstrap loop.
6. Output the final metrics to a JSON file at `/home/user/results.json`. The JSON must contain exactly these keys: `"distance"`, `"ci_lower"`, `"ci_upper"`. The values should be floats rounded to exactly 4 decimal places.

Use standard data science libraries (`numpy`, `pandas`, `scipy`) which are available in your environment.