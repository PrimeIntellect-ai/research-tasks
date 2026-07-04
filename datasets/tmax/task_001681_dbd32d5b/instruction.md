You are a data scientist debugging a linear model fitting pipeline that sometimes fails on near-singular, highly collinear inputs. You need to write a Go program to estimate the 95% confidence intervals of the model coefficients using bootstrapping, while tracking the solver's convergence/success rate, and compare it against a reference dataset.

The workspace at `/home/user` contains:
- `X.csv`: A 100x2 feature matrix (comma-separated, no header).
- `y.csv`: A 100x1 target vector (comma-separated, no header).
- `ref_w0.txt`: A plain text file containing a single float, which is the reference true coefficient for the first feature.

Write a Go program at `/home/user/bootstrapper.go` that performs the following steps:
1. Initialize a Go module in `/home/user` (e.g., `go mod init bootstrapper`) and fetch `gonum.org/v1/gonum`.
2. Read `X.csv` into a Gonum `mat.Dense` matrix (100 rows, 2 columns) and `y.csv` into a `mat.VecDense` vector (100 rows).
3. Perform a Bootstrap procedure with exactly `B = 1000` iterations to estimate the coefficients $w$ in the linear model $Xw = y$.
   - **Crucial:** Use a local random generator seeded with 42: `rng := rand.New(rand.NewSource(42))` (using `math/rand`).
   - For each iteration (from `i = 0` to `999`), generate exactly 100 random row indices using `rng.Intn(100)`.
   - Build the bootstrap sample matrices $X_{boot}$ and $y_{boot}$ by extracting the sampled rows from $X$ and $y$.
4. Attempt to solve $X_{boot} w = y_{boot}$ using Gonum's `(*mat.VecDense).SolveVec(X_boot, y_boot)`. 
   - Because $X$ is highly collinear, some bootstrap samples may be computationally singular and `SolveVec` will return an error (convergence/stability failure).
   - If `SolveVec` returns an error, discard this iteration (do not add its coefficients to your results).
   - Keep track of the solver's `success_rate` (number of successful solves / 1000).
5. Extract the first coefficient ($w_0$) from all *successful* iterations and sort them in ascending order.
6. Calculate the 95% Bootstrap Confidence Interval (2.5th and 97.5th percentiles) for $w_0$. 
   - Use `gonum.org/v1/gonum/stat`'s `Quantile` function: `stat.Quantile(p, stat.Empirical, sorted_w0, nil)` for `p=0.025` and `p=0.975`.
7. Read the reference value from `ref_w0.txt`. Determine if this reference value falls within the computed inclusive confidence interval `[ci_lower, ci_upper]`.
8. Output the results to `/home/user/result.json` in the following exact format:
```json
{
  "success_rate": 0.854,
  "ci_lower": -15.2345,
  "ci_upper": 25.1023,
  "ref_in_ci": true
}
```

Run your code to produce `result.json`.