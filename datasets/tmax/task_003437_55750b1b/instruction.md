You are assisting a researcher who is organizing and analyzing a large-scale sensor dataset. The data consists of multi-dimensional sensor readings stored in a raw binary format for efficient storage, and the researcher needs to perform an analysis of the data's variance across different subsets (folds) to evaluate the stability of the readings. 

Your task is to build a reproducible data processing pipeline using C and Bash.

**Dataset details:**
- Location: `/home/user/dataset.bin`
- Format: Raw binary file containing 64-bit IEEE 754 floating-point numbers (`double`).
- Dimensions: 10,000 rows and 50 columns, stored in row-major order.

**Instructions:**
1. **Write a C program** at `/home/user/compute_variance.c` that computes the trace of the covariance matrix (i.e., the sum of the sample variances of all columns) for a specific contiguous block of rows in the binary file.
    - The program should be compiled to `/home/user/compute_variance`.
    - It must accept exactly 4 command-line arguments: `<binary_file_path> <total_columns> <start_row> <num_rows>`.
    - Note: Use the sample variance formula with Bessel's correction (divide by `N - 1` where N is `num_rows`).
    - The program should print only the final trace value as a floating-point number (e.g., `%f` or `%lf` format) to standard output.

2. **Create a reproducible Bash pipeline** at `/home/user/evaluate.sh` that simulates a 5-fold cross-validation split over the dataset.
    - The script must compile `compute_variance.c` using `gcc` with standard optimization flags (e.g., `-O2`).
    - It should divide the 10,000 rows into 5 equal, contiguous folds of 2,000 rows each (Fold 0: rows 0-1999, Fold 1: rows 2000-3999, etc.).
    - For each fold, it must invoke `./compute_variance` to calculate the trace of the covariance matrix for that specific 2,000-row block.
    - The script must write the results to a CSV file located at `/home/user/fold_variances.csv`.

**Output Format for `/home/user/fold_variances.csv`:**
The CSV must have a header line and 5 data lines corresponding to folds 0 through 4.
```csv
Fold,Trace
0,50.123456
1,49.876543
2,50.456789
3,50.000111
4,49.999888
```
*(Note: Do not worry about the exact number of decimal places, as long as the numbers are accurate to at least 4 decimal places.)*

Ensure that your Bash script has executable permissions and can be run directly via `bash /home/user/evaluate.sh`.