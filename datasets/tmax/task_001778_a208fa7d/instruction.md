You are a Machine Learning Engineer preparing to evaluate the stability of a Bayesian-inspired Ridge Regression model on a small dataset. You need to use bootstrap resampling to estimate the mean and standard deviation of the model's single weight parameter.

Write a C++ program at `/home/user/ridge_bootstrap.cpp` that does the following:

1. **Read Dataset**: Read the dataset from `/home/user/training_data.csv`. The file has a header line `x,y` followed by 5 rows of float values.
2. **Ridge Regression**: Implement a 1D Ridge Regression model (which acts as a Gaussian prior on the weights). Because we assume the intercept is 0, the weight $w$ is calculated using linear algebra as:
   $$w = \frac{\sum_{i=1}^{N} x_i y_i}{\sum_{i=1}^{N} x_i^2 + \lambda}$$
   Use $\lambda = 2.0$.
3. **Bootstrap Resampling**: Generate 1000 bootstrap datasets. Each bootstrap dataset must consist of $N$ pairs of $(x, y)$ sampled *with replacement* from the original dataset (where $N$ is the size of the original dataset, i.e., 5).
4. **Custom RNG for Reproducibility**: To ensure exact reproducibility across different C++ compilers, DO NOT use `std::mt19937` or `std::uniform_int_distribution`. Instead, implement this exact Linear Congruential Generator to select indices:
   ```cpp
   uint64_t current_seed = 42;
   uint64_t next_random() {
       current_seed = (1103515245 * current_seed + 12345) % 2147483648;
       return current_seed;
   }
   int get_index(int N) {
       return next_random() % N;
   }
   ```
   For each of the 1000 bootstrap iterations, draw $N$ indices using `get_index(N)`. Compute $w$ for each bootstrap sample.
5. **Evaluation**: Calculate the mean and the *sample* standard deviation (using $M-1$ in the denominator, where $M=1000$) of the 1000 calculated $w$ values.
6. **Output**: Write the final statistics to `/home/user/bootstrap_results.txt` exactly in this format (rounded to 4 decimal places):
   ```
   Mean: <value>
   StdDev: <value>
   ```

**Setup:**
You must first create the `/home/user/training_data.csv` file with the following contents:
```csv
x,y
1.5,2.1
2.0,3.9
3.1,6.0
4.5,8.8
5.0,10.1
```

Compile and run your C++ script to generate `/home/user/bootstrap_results.txt`.