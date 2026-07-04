You are acting as a bioinformatics analyst. You have received a dataset containing the GC content (a fraction between 0 and 1) and the Sequence Length (in base pairs) for several filtered DNA sequences from a recent sequencing run. You hypothesize that there is a linear relationship between GC content and Sequence Length in this specific filtered subset.

Your task is to write a C program that calculates the Ordinary Least Squares (OLS) linear regression slope for this data and estimates the 95% confidence interval for the slope using bootstrapping.

The dataset is located at `/home/user/seq_data.csv` and contains a header row. 
Format:
```csv
GC,Length
0.35,120
0.41,135
...
```

Write a C program at `/home/user/bootstrap_regression.c` that performs the following:
1. Reads the dataset into memory (there are exactly 8 data rows).
2. Calculates the OLS slope `m` where `Length = m * GC + c`.
3. Sets the random seed exactly once at the start of your main function using `srand(42);`.
4. Performs a bootstrap analysis with exactly `10000` iterations to find the 95% confidence interval of the slope.
5. In each iteration, create a resampled dataset of the same size (8 rows) by sampling with replacement from the original dataset. Use `rand() % 8` to select the row index for each of the 8 samples in the resampled dataset. Do this 8 times sequentially for each iteration.
6. Calculate the OLS slope for the resampled dataset and store it.
7. After 10,000 iterations, sort the 10,000 bootstrapped slopes in ascending order.
8. Determine the 95% confidence interval using the percentile method. Specifically, use the value at array index `250` as the lower bound (2.5th percentile) and the value at array index `9749` as the upper bound (97.5th percentile).
9. Print the results to a file named `/home/user/regression_results.txt` exactly in this format (rounded to 2 decimal places):
`Slope: [original_slope], 95% CI: [[lower_bound], [upper_bound]]`

Compile your code, run it, and ensure `/home/user/regression_results.txt` is generated successfully. Ensure you include standard math libraries during compilation (`-lm`).