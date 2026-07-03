You are a data scientist working on cleaning noisy sensor data. The data contains linear trends but is corrupted by severe outlier measurements. You need to build a reproducible, high-performance pipeline in C and Bash to compute a linear model, track experiments, and filter out the noise.

Your objective is to write a C program and a Bash pipeline that processes multiple CSV datasets, computes an Ordinary Least Squares (OLS) regression line, identifies outliers based on residuals, and tracks the results.

### Task Requirements:

1. **The C Program (`/home/user/cleaner.c`)**
   Write a C program that accepts two command-line arguments: an input CSV file path and an output CSV file path.
   The input CSV files contain two columns of floats: `x,y` (no header).
   The program must do the following:
   * Read all `x,y` pairs from the input file. You may assume no file has more than 10,000 rows.
   * Calculate the OLS regression line: $y = mx + b$
     * $m = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}$
     * $b = \bar{y} - m\bar{x}$
     (Where $\bar{x}$ and $\bar{y}$ are the means of x and y).
   * Calculate the absolute residual for every point: $r_i = |y_i - (mx_i + b)|$.
   * Identify outliers: Any point with $r_i > 15.0$ is considered an outlier.
   * Write all *non-outlier* points to the specified output CSV file in the same `x,y` format (formatted to 4 decimal places, e.g., `%.4f,%.4f`).
   * Print exactly one line to `stdout` containing the summary metrics formatted as:
     `[INPUT_FILENAME],m=[m_val],b=[b_val],outliers=[count]`
     *(Format `m_val` and `b_val` to 4 decimal places).*

2. **The Bash Pipeline (`/home/user/run_experiments.sh`)**
   Write a bash script that does the following:
   * Compiles `/home/user/cleaner.c` into an executable named `/home/user/cleaner` using `gcc` (include the math library with `-lm`).
   * Creates an empty tracking file at `/home/user/experiment_log.csv` and writes the header: `dataset,slope,intercept,removed_outliers`.
   * Finds all `.csv` files inside `/home/user/raw_data/`.
   * For each dataset (e.g., `/home/user/raw_data/sensor1.csv`):
     * Runs the `cleaner` executable, saving the cleaned data to `/home/user/cleaned_data/clean_[FILENAME]` (e.g., `/home/user/cleaned_data/clean_sensor1.csv`).
     * Parses the stdout of the C program to append a row to `/home/user/experiment_log.csv` in the format: `sensor1.csv,1.2345,0.1234,5`. (Extract the exact values from the C program's stdout).

### Directories & Setup:
* The raw datasets are located in `/home/user/raw_data/`.
* You must create the `/home/user/cleaned_data/` directory.
* Ensure `/home/user/run_experiments.sh` is executable.

Complete the task by creating the C source file and the Bash script as specified. You can run your bash script to test it and ensure `experiment_log.csv` matches the required structure.