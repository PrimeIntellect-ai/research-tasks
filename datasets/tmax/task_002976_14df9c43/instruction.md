You are an MLOps engineer tasked with reconstructing a critical data preprocessing pipeline. The original code was lost, but the original author left an audio log describing the hyperparameters, and we have a strict automated testing framework to validate your implementation.

First, locate the audio log at `/app/experiment_log.wav`. Use any available tool (e.g., `ffmpeg`, `whisper`, or Python speech recognition libraries) to transcribe it. The audio contains the specific Z-score threshold used for outlier clipping.

Next, write a Python script at `/home/user/pipeline.py` that reads a headless CSV of floating-point numbers from standard input (`sys.stdin`) and outputs a processed covariance matrix to standard output (`sys.stdout`). The input CSV will always have 10 columns, but the number of rows will vary. Some values will be missing (represented by empty strings).

Your pipeline must strictly perform the following steps using `numpy` (float64 precision):
1. **Missing Value Handling:** Read the data. For each column, compute the mean (ignoring missing values). Replace all missing values in that column with this mean.
2. **Outlier Clipping:** After imputation, compute the new mean and sample standard deviation (`ddof=1`) for each column. Clip any values in the column that fall outside `mean ± Z * std` to exactly the boundary values (`mean + Z * std` or `mean - Z * std`). Extract the value of `Z` from the audio log.
3. **Standardization:** After clipping, compute the final mean and sample standard deviation (`ddof=1`) for each column. Standardize the data by subtracting the mean and dividing by the standard deviation.
4. **Dimensionality Reduction Prep (Covariance):** Compute the 10x10 covariance matrix of the standardized dataset (using `numpy.cov` with `rowvar=False` and `ddof=1`).
5. **Output:** Round the resulting 10x10 covariance matrix to exactly 4 decimal places using `numpy.round`. Print the matrix to standard output as a CSV (comma-separated, no spaces, 10 lines, 10 values per line, trailing zeros included if necessary to show 4 decimal places, e.g., `1.0000`).

Additionally, there is a script at `/home/user/plot_cov.py` that is supposed to visualize this matrix, but it currently produces a completely blank plot due to a backend misconfiguration in our headless Linux environment. Fix `/home/user/plot_cov.py` so that it successfully saves a non-blank plot to `/home/user/cov_plot.png`.

Your `/home/user/pipeline.py` script will be aggressively tested against thousands of randomized inputs to ensure bit-exact equivalence with the original oracle pipeline.