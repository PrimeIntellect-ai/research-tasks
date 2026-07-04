You are an ML Engineer preparing a high-performance C pipeline for training data analysis. We are migrating our pre-processing pipeline from pandas to C for speed, but we are running into issues with data type corruption and schema enforcement. 

Your objective is to write a C program that enforces our strict data schema, tracks data quality metrics, and computes a correlation matrix using a vendored library.

Here are the requirements:

1. **Analysis Environment Setup**:
   We vendor a lightweight C library called `fastcovar` for matrix math, located in `/app/fastcovar-0.3`. However, the current vendored version has a bug: a recent botched patch causes it to silently truncate floating-point intermediate values to integers during computation, completely ruining the correlation results (similar to silent NaN-to-float conversions in pandas, but in reverse). 
   - You must locate the source of this type truncation in the `fastcovar` headers, fix it to use `double` precision, and compile the static library (`make`).

2. **Primary Implementation**:
   Write a C program at `/home/user/process_data.c` and compile it to `/home/user/process_data`.
   It must read a CSV without a header from `stdin`. The CSV will always have exactly 3 columns.
   
3. **Data Schema Enforcement**:
   For every row read:
   - If any column contains the string `NaN` (case-sensitive) or cannot be parsed as a float, the row must be dropped.
   - If any column's value is strictly less than `-1000.0` or strictly greater than `1000.0`, the row must be dropped.

4. **Experiment Tracking**:
   To track data quality, your program must print the following exactly to `stderr` upon reading all input:
   `Valid rows: <N>, Dropped rows: <M>`

5. **Correlation Analysis**:
   For the valid rows, compute the 3x3 Pearson correlation matrix using the `fastcovar` library. (Assume the fixed library exposes a function `void compute_pearson_3x3(double* col1, double* col2, double* col3, int n, double out_matrix[3][3]);` inside `fastcovar.h`).
   Print the resulting 3x3 matrix to `stdout`, comma-separated, formatted to exactly 4 decimal places (`%.4f`). Each row of the matrix should be on a new line.

Ensure your compiled executable `/home/user/process_data` statically links the fixed `libfastcovar.a` and correctly handles EOF from stdin.