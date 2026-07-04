You are a researcher organizing a dataset using only standard Linux command-line tools (Bash, Awk, Sed, etc.). You must process a dataset, enforce its schema, compute a correlation, and calculate a confidence interval. Do not use Python, R, or any other programming languages besides shell scripts and standard Unix utilities (like `awk`, `grep`).

The raw dataset is located at `/home/user/raw_data.csv` with a header row `A,B,C,D`.

Your objectives:

1. **Schema Enforcement (`/home/user/clean.sh`)**:
   Write a script that reads `/home/user/raw_data.csv` and outputs valid rows to `/home/user/clean_data.csv`.
   A valid row must meet these criteria:
   - Exactly 4 comma-separated columns.
   - For data rows (excluding the header), columns A, B, and C must be purely numeric (integers or decimals, can be negative). Column D can be anything.
   - The header row must be preserved as the first line.

2. **Correlation Analysis (`/home/user/correlation.sh`)**:
   Write a script that reads `/home/user/clean_data.csv` and computes the Pearson correlation coefficient between Column A and Column B.
   - Use the population formula for standard deviation.
   - Print the final correlation value rounded to 4 decimal places (e.g., `0.9521`) to standard output.
   - Save the output of this script to `/home/user/cor.txt`.

3. **Hypothesis Testing / Confidence Intervals (`/home/user/ci.sh`)**:
   Write a script that reads `/home/user/clean_data.csv` and computes the Mean and 95% Confidence Interval for Column C.
   - Use the formula: `CI = Mean ± 1.96 * (StdDev / sqrt(N))`
   - Use the population standard deviation for `StdDev`.
   - `N` is the number of valid data rows.
   - Print the output in the format `Mean,Lower,Upper` rounded to 4 decimal places (e.g., `10.5000,9.2000,11.8000`) to standard output.
   - Save the output of this script to `/home/user/ci.txt`.

Constraints:
- All tools must be standard POSIX/Linux utilities (bash, awk, grep, etc.). No Python or R.
- Execute your scripts and ensure `clean_data.csv`, `cor.txt`, and `ci.txt` are created with the correct values.