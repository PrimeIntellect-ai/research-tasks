You are acting as an AI assistant for a data scientist. We are trying to fit theoretical probability distributions to an observed dataset to build a predictive model.

We have an internal Go library for computing probability distribution distance metrics, located at `/app/distmetric`. However, the library is currently broken. Someone recently made a commit that broke the build and caused the KL divergence calculation to yield incorrect (often negative) results.

Your tasks are as follows:

1. **Fix the vendored package**: 
   - Navigate to `/app/distmetric`.
   - Fix any build issues (check `go.mod` and syntax errors).
   - Fix the logical bug in `kl.go`'s `KLDivergence` function. It currently computes the sum of `p[i] * math.Log(q[i]/p[i])`, which is the negative of the correct Kullback-Leibler divergence. Update it to standard form: `sum += p[i] * math.Log(p[i]/q[i])`.

2. **Fit the model**:
   - We have an observed dataset of 10,000 samples stored in a plain text file at `/home/user/observed_data.txt` (one float per line).
   - Write a Go program at `/home/user/fitter.go` that reads this dataset and creates a discrete histogram (probability mass function) using 100 equally spaced bins between the minimum and maximum values of the dataset.
   - Use the `distmetric` package to compute the KL divergence between this empirical PMF and a theoretical Normal distribution's PMF evaluated at the same bin centers. (Ensure both PMFs sum to 1.0 to avoid invalid KL divergence).
   - Implement a basic grid search, gradient descent, or iterative refinement to find the optimal parameters (`mu` and `sigma`) for the Normal distribution that minimize the KL divergence to the empirical data.
   - Search bounds to consider: `mu` in [0.0, 10.0], `sigma` in [0.1, 5.0].

3. **Output**:
   - Write your optimized parameters and the final KL divergence to a JSON file at `/home/user/result.json` strictly in the following format:
     ```json
     {
       "mu": 5.123,
       "sigma": 1.987,
       "kl_divergence": 0.004
     }
     ```

Ensure your Go code can be run via `go run /home/user/fitter.go`. Do not use external libraries for the optimization step; standard Go math and basic logic are sufficient.