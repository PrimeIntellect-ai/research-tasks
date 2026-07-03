You are an AI assistant helping a bioinformatics analyst process time-series sequence abundance data.

We have a dataset `/home/user/sequence_data.csv` recording the abundance of various RNA sequences over 5 timepoints. We want to identify the dominant temporal trend using matrix decomposition and then fit an exponential decay model to that trend using Markov Chain Monte Carlo (MCMC) sampling.

Your task is to write a Go program that performs this analysis. 

**Step 1: Setup and Reshaping**
1. Initialize a Go module in `/home/user/seq_analysis`.
2. Write a Go program `analyze.go` that reads `/home/user/sequence_data.csv`. The CSV has a header: `SeqID,T0,T1,T2,T3,T4`.
3. Parse the data into an $N \times 5$ observation matrix.
4. Mean-center the data *per sequence* (subtract the mean of each row from its elements).

**Step 2: Matrix Decomposition**
1. Use the `gonum.org/v1/gonum/mat` package to perform a Singular Value Decomposition (SVD) on the centered matrix.
2. Extract the first principal component's temporal weights: the first column of the right singular matrix $V$ (or the first row of $V^T$). Let's call this vector $v$ (length 5).
3. Normalize $v$ such that its first element is exactly 1.0 (i.e., $y_t = v_t / v_0$). These normalized values $y_0, y_1, y_2, y_3, y_4$ represent the dominant temporal trend.
4. Identify the 3 `SeqID`s with the highest absolute loadings in the first left singular vector $U$ (the first column of $U$). Write these 3 IDs, one per line, to `/home/user/top_sequences.txt`.

**Step 3: MCMC Sampling & Curve Fitting**
We assume the normalized trend follows an exponential decay: $y_t \approx e^{-\lambda t}$ for $t \in \{0, 1, 2, 3, 4\}$.
Implement a Metropolis-Hastings MCMC sampler in Go to estimate the posterior mean of $\lambda$:
1. **Target Log-Likelihood:** $\log P(y | \lambda) = -\sum_{t=0}^4 \frac{(y_t - e^{-\lambda t})^2}{2 \sigma^2}$, where $\sigma^2 = 0.01$.
2. **Prior:** Uniform distribution for $\lambda \in [0, 5]$. (Log-prior is 0 if $0 \le \lambda \le 5$, else $-\infty$).
3. **Proposal Distribution:** Normal distribution centered at the current $\lambda$ with standard deviation 0.05.
4. **Initialization:** Start at $\lambda_{curr} = 1.0$.
5. **RNG Setup:** Use `rand.New(rand.NewSource(42))` from `math/rand` to generate your proposals and acceptance uniform variables to ensure reproducibility. *First* draw the proposal, *then* draw the uniform acceptance threshold.
6. **Iterations:** Run exactly 50,000 iterations (after the initial state).
7. **Burn-in:** Discard the first 10,000 iterations.
8. Calculate the mean of $\lambda$ from the remaining 40,000 samples. Write this mean, formatted to exactly 4 decimal places (e.g., `0.3452`), to `/home/user/lambda_mean.txt`.

Ensure your Go program compiles, runs successfully, and creates the required output files. Use `go mod tidy` to manage dependencies.