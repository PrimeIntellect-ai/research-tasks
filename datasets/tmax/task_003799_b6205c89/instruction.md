You are an AI assistant helping a performance engineer analyze application latencies. 

I have collected response time data (in milliseconds) from our critical API endpoint. The data is stored in `/home/user/latencies.txt` as a single column of floating-point numbers. We suspect the latencies are drawn from a 2-component Gaussian Mixture Model (GMM), representing "cache hit" (fast) and "cache miss" (slow) requests.

We assume the model is:
$p(x) = w \cdot \mathcal{N}(x | \mu_1, \sigma^2=1.0) + (1-w) \cdot \mathcal{N}(x | \mu_2, \sigma^2=1.0)$
where $w$ is the weight of the first component ($0 \le w \le 1$), and $\mu_1 < \mu_2$. The variances are assumed to be fixed at 1.0.

Your task is to write a C program at `/home/user/mcmc_profiler.c` that does the following:
1. Reads the data from `/home/user/latencies.txt`.
2. Implements a Metropolis-Hastings MCMC sampler from scratch to estimate the posterior distribution of $w, \mu_1,$ and $\mu_2$. 
   - Use uniform priors: $w \in [0, 1]$, $\mu_1 \in [0, 20]$, $\mu_2 \in [0, 20]$. Apply the constraint $\mu_1 < \mu_2$ by rejecting any proposals where $\mu_1 \ge \mu_2$.
   - Use a Gaussian random walk proposal for each parameter with a standard deviation of 0.1.
   - Run the MCMC chain for exactly 50,000 iterations.
   - Discard the first 10,000 iterations as burn-in.
   - Calculate the posterior mean for $w, \mu_1,$ and $\mu_2$ using the remaining 40,000 samples.
3. Computes the probability distribution distance. Specifically, calculate the discrete Kullback-Leibler (KL) divergence between the empirical latency distribution and the fitted GMM distribution:
   - Create a histogram of the empirical data using exactly 50 bins evenly spaced between `x_min = 0.0` and `x_max = 20.0`.
   - The empirical probability $P_i$ of bin $i$ is the count of data points falling in bin $i$ divided by the total number of data points. (A point $x$ falls in bin $i$ if $edges[i] \le x < edges[i+1]$. Data exactly at $20.0$ falls in the last bin).
   - The estimated probability $Q_i$ of bin $i$ is approximated by evaluating the PDF of the fitted GMM (using the posterior means of $w, \mu_1, \mu_2$) at the **midpoint** of bin $i$, and multiplying by the bin width ($20.0 / 50$). Normalize $Q$ so it sums to exactly 1 over the 50 bins.
   - Compute $D_{KL}(P || Q) = \sum_{i} P_i \ln(P_i / Q_i)$. Skip bins where $P_i = 0$.
4. Writes the results to `/home/user/profiler_results.txt` in the following format (rounding to 3 decimal places):
   ```
   w: 0.XXX
   mu1: X.XXX
   mu2: X.XXX
   kl_divergence: 0.XXX
   ```

Compile your code with `gcc -O3 -lm mcmc_profiler.c -o mcmc_profiler`, run it, and ensure the output file is generated correctly.