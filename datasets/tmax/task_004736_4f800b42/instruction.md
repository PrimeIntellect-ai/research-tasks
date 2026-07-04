I need to clean up a dataset of sensor readings by identifying redundant, highly correlated features. However, the dataset is massive, and computing the exact correlation matrix across all rows is computationally expensive. I want to use a bootstrap sampling method to approximate the correlation matrix efficiently.

I have a vendored C library called `fastcov` version 1.2.0 located at `/app/fastcov-1.2.0` that provides fast primitives for computing covariance and standard deviation. Unfortunately, it's currently broken—it fails to compile out of the box due to some missing configuration in its Makefile.

Here is what you need to do:
1. Fix the `fastcov` library in `/app/fastcov-1.2.0` so it compiles successfully into a shared library (`libfastcov.so`). 
2. Write a C program at `/home/user/dataset_cleaner.c` that dynamically links against `libfastcov.so`.
3. Your C program must read the dataset located at `/app/data/sensor_readings.csv`. The file has no header, 5 columns (features), and 50,000 rows of floating-point numbers.
4. Implement a bootstrap sampling method in your C code: randomly sample 2,000 rows *with replacement* from the dataset. Compute the 5x5 correlation matrix for this sample using the `fastcov` library functions. Repeat this process 100 times, and compute the element-wise average of these 100 correlation matrices to get your final robust approximation.
5. Save the final averaged 5x5 correlation matrix to `/home/user/correlations.csv`. The format should be exactly 5 lines, each containing 5 comma-separated floats (e.g., formatted with `%.6f`).

The accuracy of your approximation is critical. Your output matrix will be evaluated against the true population correlation matrix. You must achieve a Mean Squared Error (MSE) of less than 0.005.

Note: The `fastcov` library provides a header `fastcov.h` with the following signatures you should use:
- `double compute_covariance(double* x, double* y, int n);`
- `double compute_stddev(double* x, int n);`
*(Recall that correlation(x, y) = covariance(x, y) / (stddev(x) * stddev(y)))*