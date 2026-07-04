You are a Machine Learning Engineer preparing a dataset for a new training pipeline. You need to join raw data sources, filter out noisy outliers using a pre-trained linear regression model, and benchmark the inference speed of your filtering implementation.

Your workspace contains the following files in `/home/user/data`:
1. `features.csv` - Contains an `ID` column and two feature columns `x1` and `x2`.
2. `labels.csv` - Contains an `ID` column and a target variable `y`.
3. `weights.txt` - Contains three lines representing the learned linear regression weights: $w_0$ (bias), $w_1$, and $w_2$.

Please perform the following steps:

1. **Data Joining:** Join `features.csv` and `labels.csv` on the `ID` column. Save the result as `/home/user/data/joined.csv` with the format `ID,x1,x2,y` (no headers, comma-separated).

2. **Library Configuration:** Install the OpenBLAS development libraries on the system (using `apt-get`, you have passwordless sudo).

3. **C Implementation:** Write a C program at `/home/user/filter.c` that does the following:
   - Reads `joined.csv` and `weights.txt`.
   - Uses the OpenBLAS function `cblas_ddot` (from `cblas.h`) to compute the linear regression prediction for each row: $\hat{y} = w_0 \cdot 1.0 + w_1 \cdot x_1 + w_2 \cdot x_2$. Note: you must set up an array `[1.0, x1, x2]` to dot-product with `[w0, w1, w2]`.
   - Computes the squared error $(y - \hat{y})^2$.
   - Classifies the row as "valid" if the squared error is $< 2.0$, otherwise it is an "outlier".
   - Writes all "valid" rows to `/home/user/filtered.csv` in the format `ID,x1,x2,y,y_hat` (format `y_hat` to exactly 3 decimal places).
   - Measures the CPU time taken *only* by the inference and classification loop using `clock()`. Run this loop 10,000 times (process the same dataset 10,000 times in memory) to get a measurable benchmark.
   - Writes the benchmarked time (in seconds, as a floating point number) to `/home/user/benchmark.txt`.

4. **Build and Execute:** Compile your program to `/home/user/filter` linking against OpenBLAS, and run it to produce `/home/user/filtered.csv` and `/home/user/benchmark.txt`.

Ensure your C code properly handles file I/O and links the library correctly.