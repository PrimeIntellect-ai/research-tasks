You are tasked with debugging and extending a bioinformatics analysis tool written in Go, which analyzes sequence properties based on k-mer frequency matrices.

You have been provided with a Go module located in `/home/user/src/mahalanobis`. This tool reads a CSV file of k-mer frequencies, calculates the dataset's covariance matrix, inverts it to calculate the Mahalanobis distance of each sample from the origin, and then outputs the mean distance for Group A and Group B. 

However, the sequence input matrix `/home/user/data/kmer_counts.csv` contains near-singular collinearities (due to perfectly correlated k-mers), causing the matrix inversion to fail.

Your objectives:
1. **Fix the Go Tool**: Modify `/home/user/src/mahalanobis/main.go` to apply Ridge regularization. Add exactly `0.0001` to each diagonal element of the covariance matrix *before* attempting the inversion.
2. **Compile**: Compile the modified Go tool into an executable named `mahalanobis_calc` in the directory `/home/user/bin/`.
3. **Bootstrap Confidence Intervals**: Enhance the tool (or write an additional wrapper script in Go or bash) to perform a Bootstrap analysis to compare Group A (the first 50 rows of the CSV) and Group B (the remaining 50 rows).
   - Resample the rows of Group A with replacement to form a bootstrap sample of size 50.
   - Resample the rows of Group B with replacement to form a bootstrap sample of size 50.
   - Calculate the difference in mean Mahalanobis distance: $\Delta = \text{Mean}_A - \text{Mean}_B$.
   - Repeat this for exactly `10,000` bootstrap iterations.
   - Note: Use the regularized inverse covariance matrix of the *original full dataset* for all distance calculations. Do not recompute the covariance matrix for each bootstrap resample.
4. **Statistical Hypothesis Comparison**: Calculate the two-sided empirical p-value for the null hypothesis $H_0: \mu_A = \mu_B$ based on your bootstrap distribution.
5. **Output**: Save your results in `/home/user/results.json` strictly matching this format:
```json
{
  "ci_lower": 1.234, 
  "ci_upper": 5.678,
  "p_value": 0.045
}
```
*Where `ci_lower` and `ci_upper` are the 2.5th and 97.5th percentiles of the bootstrap $\Delta$ distribution respectively.*

*Constraints & Notes:*
- Ensure `/home/user/bin/` exists before building.
- Set your random seed to `42` (using `rand.Seed(42)` or `rand.New(rand.NewSource(42))`) before beginning the bootstrap loop to ensure reproducible percentiles.
- All distances should be squared Mahalanobis distances $D^2 = x^T \Sigma^{-1} x$, where $x$ is the sample vector and $\Sigma^{-1}$ is the regularized inverse covariance matrix.