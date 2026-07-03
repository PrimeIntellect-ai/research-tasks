I am a researcher organizing a set of continuous observations, and I need a lightweight, fast ETL and analysis pipeline written in C. 

Please perform the following steps:

1. Write a C program in `/home/user/compute_cov.c` that reads a CSV dataset and computes the sample covariance matrix.
   - The compiled executable should be named `compute_cov` and placed in `/home/user/`.
   - It should accept exactly two command-line arguments: the input CSV file path and the output text file path. Example: `./compute_cov input.csv output.txt`
   - The input CSV will have exactly 3 columns of floating-point numbers and NO header row.
   - Compute the sample covariance matrix (using `N - 1` in the denominator).
   - The output file must contain the 3x3 covariance matrix. Each row of the matrix should be printed on a new line. The values in each row must be separated by a single space and formatted to exactly 4 decimal places (using `%.4f`).

2. Create a bash script `/home/user/test_reproducibility.sh` to test the stability of the dataset.
   - The script should take the main dataset `/home/user/dataset.csv` (which has 10 lines) and split it into two halves: the first 5 lines into `split1.csv` and the last 5 lines into `split2.csv` (both in `/home/user/`).
   - Run the `./compute_cov` program on both splits to produce `/home/user/cov1.txt` and `/home/user/cov2.txt`.
   - The script must be executable.

Please compile the C program and run your script so that `cov1.txt` and `cov2.txt` are generated. Ensure your C code handles file I/O properly and frees any allocated memory.