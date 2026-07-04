You are a machine learning engineer tasked with preparing high-dimensional training data and benchmarking the inference transformation step. We need to reduce the dimensionality of our dataset for a low-latency inference system. 

You have been provided with two files in your home directory:
- `/home/user/train_data.csv`: A dataset with 1000 rows and 50 columns (features), no header.
- `/home/user/test_data.csv`: A dataset with 10000 rows and 50 columns, no header.

Your task is to write a script in a language of your choice (e.g., Python using numpy) to do the following:

1. **Feature Standardization**: Calculate the mean and standard deviation for each column in `train_data.csv`. Standardize both `train_data.csv` and `test_data.csv` using the **training data's** mean and standard deviation (i.e., `(x - mean) / std`).
2. **Dimensionality Reduction**: Perform Principal Component Analysis (PCA) on the standardized training data. 
3. **Feature Selection**: Determine the minimum number of principal components ($k$) required to explain strictly **greater than 90% (> 0.90)** of the total variance in the training data.
4. **Benchmarking**: Project the standardized `test_data.csv` into the new $k$-dimensional space using matrix multiplication. Benchmark the time it takes to perform **just the projection matrix multiplication** on the `test_data.csv` (excluding standardizing and I/O loading times). Run this matrix multiplication 100 times and calculate the average execution time in milliseconds.

Finally, generate a JSON file at `/home/user/results.json` with the following structure:
```json
{
  "k": 12,
  "variance_explained": 0.91234,
  "benchmark_ms": 1.25
}
```
*Note: `k` must be an integer, `variance_explained` must be a float representing the exact cumulative explained variance ratio of the $k$ components (between 0.90 and 1.0), and `benchmark_ms` must be a float representing the average time in milliseconds.*

Write and execute the necessary code to fulfill these requirements. Install any libraries you need using the system's package manager or pip.