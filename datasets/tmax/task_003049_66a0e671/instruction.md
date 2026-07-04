You are a performance engineer analyzing a new nonlinear queuing system. You have observations of the system's load parameter ($\lambda$) and a performance metric ($x$). Theoretical analysis shows that the expected metric $x_{pred}$ satisfies the nonlinear equation:
$x_{pred}^3 + \mu \cdot x_{pred} - \lambda = 0$
where $\mu$ is an unknown system parameter. The observed metric $x$ is assumed to be normally distributed around $x_{pred}$ with unknown standard deviation $\sigma$.

Your task is to estimate the posterior means of $\mu$ and $\sigma$ using Markov Chain Monte Carlo (MCMC) and profile your application's performance.

Write a Go program at `/home/user/queuing_mcmc.go` that does the following:
1. Reads the dataset from `/home/user/observations.csv` (contains headers `lambda,x`).
2. Runs 4 parallel MCMC chains (using goroutines and a WaitGroup) to estimate the posterior distribution of $\mu$ and $\sigma$. 
3. Each chain must:
    - Run for exactly 15,000 iterations, discarding the first 5,000 as burn-in.
    - Use independent uniform priors: $\mu \sim U(0, 10)$ and $\sigma \sim U(0.01, 2.0)$.
    - Use independent normal proposal distributions centered at the current values with standard deviations 0.1 for $\mu$ and 0.05 for $\sigma$.
    - Start at initial values: $\mu_0 = 5.0$, $\sigma_0 = 1.0$.
    - For each proposed $\mu$, solve the nonlinear equation $x_{pred}^3 + \mu \cdot x_{pred} - \lambda = 0$ for each $\lambda$ using Newton-Raphson (start initial guess $x=1.0$, tolerance $10^{-6}$, max 100 iterations) to evaluate the log-likelihood of the observations.
4. Integrate CPU profiling using the `runtime/pprof` package. Write the CPU profile to `/home/user/cpu.prof`.
5. After all chains finish, compute the mean of the posterior samples (post-burn-in) for $\mu$ and $\sigma$ within each chain, then average these means across the 4 chains.
6. Write these final two averaged values (comma-separated, $\mu$ then $\sigma$) to `/home/user/results.txt`.

Run your Go program to generate the profile and the results file.