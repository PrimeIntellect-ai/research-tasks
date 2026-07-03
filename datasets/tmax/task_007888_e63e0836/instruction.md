You are a bioinformatics analyst trying to determine if a specific genetic motif is overrepresented in a set of sequences, and how robust its occurrence count is.

You have a dataset of 1000 sequences, each of length 50, encoded as integers where 0=A, 1=C, 2=G, and 3=T.
The data is stored as a 2D NumPy array of shape `(1000, 50)` at `/home/user/sequences.npy`.

Your task is to write and run a Python script to analyze the frequency of the motif `[0, 1, 2]` (which corresponds to A-C-G). 

Perform the following three steps:

1. **Observed Count:** 
   Count the total number of times the contiguous sequence `[0, 1, 2]` appears across all rows in the dataset. 
   Save this single integer to `/home/user/observed_count.txt`.

2. **Monte Carlo Null Distribution:**
   Calculate the overall background probabilities (frequencies) of the 4 nucleotides (0, 1, 2, and 3) in the entire dataset.
   Set the random seed using `np.random.seed(42)`.
   Generate 1000 "null" matrices of the exact same shape `(1000, 50)` by randomly sampling integers 0-3 according to the calculated background probabilities.
   For each null matrix, calculate the total count of the `[0, 1, 2]` motif.
   Calculate the 95th percentile of these 1000 null counts (using `np.percentile` with default parameters).
   Save this value to `/home/user/null_95.txt`.

3. **Bootstrap Confidence Interval:**
   Now, assess the variance of the observed count by resampling the original data.
   Set the random seed using `np.random.seed(123)`.
   Perform 1000 bootstrap iterations. In each iteration, create a new matrix by sampling 1000 rows *with replacement* from the original `sequences.npy` array.
   Calculate the motif count for each of the 1000 bootstrapped matrices.
   Calculate the 95% confidence interval by finding the 2.5th and 97.5th percentiles of these bootstrap counts.
   Save these two values, separated by a comma (e.g., `450.0, 550.0`), to `/home/user/boot_ci.txt`.

Ensure all output files are placed exactly as requested in `/home/user/`.