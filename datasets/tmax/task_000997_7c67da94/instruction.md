You are a machine learning engineer preparing training data. You suspect your raw feature values follow an Exponential distribution, but you need to fit the parameter $\lambda$ robustly, compute confidence intervals, and ensure numerical stability in your pipeline. 

Write a C++ program at `/home/user/fit_dist.cpp` that performs the following tasks:

1. **Read Data**: Read 1000 floating-point numbers from `/home/user/data.txt`.
2. **Probability Distribution Distance**: Implement the Cramer-von Mises (CvM) distance between the empirical distribution of the sample and the theoretical Exponential distribution $F(x) = 1 - e^{-\lambda x}$. 
   The CvM distance formula is: $\omega^2 = \frac{1}{12n} + \sum_{i=1}^n \left( F(x_{(i)}) - \frac{2i-1}{2n} \right)^2$ where $x_{(i)}$ is the $i$-th sorted data point (1-indexed).
3. **Optimization**: Find the optimal $\lambda$ that minimizes the CvM distance. Use a simple grid search over the range $\lambda \in [0.1, 5.0]$ with a step size of $0.01$. Select the $\lambda$ that gives the minimum distance.
4. **Bootstrap Confidence Intervals**: Generate 500 bootstrap resamples (each of size 1000, sampled with replacement) from the original data. For each resample, find the optimal $\lambda$ using the same grid search method. Use the percentile method to find the 95% confidence interval (2.5th and 97.5th percentiles). 
   *Requirement*: Use `std::mt19937` initialized with the seed `42` for all random index generation (`std::uniform_int_distribution<int>(0, n-1)`).
5. **Numerical Stability Testing**: Naive evaluation of $1 - e^{-\lambda x}$ can suffer from catastrophic cancellation for very small $x$. For your optimal $\lambda$ (from step 3), compute the absolute difference between `1.0 - std::exp(-lambda * x)` and `-std::expm1(-lambda * x)` for $x = 10^{-8}$.
6. **Output**: Write the results to `/home/user/results.json` with the following exact keys (format as a simple JSON object with float values):
   - `"lambda_opt"`: The optimal $\lambda$ on the original data.
   - `"ci_lower"`: The 2.5th percentile of the bootstrap $\lambda$ estimates.
   - `"ci_upper"`: The 97.5th percentile of the bootstrap $\lambda$ estimates.
   - `"stability_diff"`: The absolute numerical difference calculated in step 5.

Compile your program using `g++ -O3 -std=c++17 /home/user/fit_dist.cpp -o /home/user/fit_dist` and run it to produce the `results.json` file.