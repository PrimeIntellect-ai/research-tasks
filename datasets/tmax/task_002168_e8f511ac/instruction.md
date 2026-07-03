You are a Machine Learning Engineer preparing a dataset for a downstream predictive model. The raw data has been corrupted with missing values and extreme outliers. Since the pipeline must be highly performant, you need to write a C program to perform robust statistical data preparation.

The raw dataset is located at `/home/user/dataset.csv`. It contains two columns of floating-point numbers, `X` and `Y`, separated by a comma. Missing values are represented by the character `?`.

Write a C program (save it as `/home/user/prepare_data.c`) that implements the following reproducible pipeline:

1. **Missing Value Handling:** Read the CSV file. Discard any row where either `X` or `Y` is `?`.
2. **Outlier Filtering:** 
   - Calculate the centroid (mean of X, mean of Y) of the remaining valid points.
   - Calculate the Euclidean distance of each point to this centroid.
   - Calculate the mean and standard deviation of these distances.
   - Filter out (discard) any point whose distance to the centroid is strictly greater than `mean_distance + (2.0 * std_dev_distance)`.
3. **Bootstrap Sampling and Correlation:**
   - Let `N` be the number of points remaining after outlier removal.
   - Initialize the standard C random number generator exactly once at the start of this step using `srand(42);`.
   - Perform exactly 10,000 bootstrap iterations.
   - In each iteration, create a bootstrap sample of size `N` by drawing points with replacement from the cleaned dataset. To select an index, use `rand() % N`.
   - Compute the Pearson correlation coefficient for this bootstrap sample. (If a bootstrap sample has a standard deviation of 0 for X or Y, treat its correlation as 0.0).
4. **Aggregation:** Calculate the mean of these 10,000 correlation coefficients.
5. **Reporting:** Write the final mean correlation coefficient to `/home/user/robust_corr.txt`, formatted to exactly four decimal places (e.g., `0.9812`).

Compile and run your C program to generate the required output file.