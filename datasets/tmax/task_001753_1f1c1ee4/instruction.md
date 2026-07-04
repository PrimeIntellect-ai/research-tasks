You are a performance engineer analyzing the execution time of a critical microservice. You have collected a trace of execution times (in milliseconds) for 10 recent requests, saved in `/home/user/trace.txt`. 

You suspect that the mean execution time $\mu$ has degraded. You need to perform a Bayesian analysis to estimate the posterior distribution of $\mu$ and test the hypothesis that $\mu > 105$ ms.

The model is defined as follows:
- The execution times $X_i$ are independent and normally distributed with unknown mean $\mu$ and known standard deviation $\sigma = 10$.
- Your prior belief for $\mu$ is a normal distribution with mean $\mu_0 = 100$ and standard deviation $\sigma_0 = 20$.

Your task is to write a C program `/home/user/analyze.c` that does the following:
1. **Analytical Solution Validation:** Calculates the exact analytical posterior mean and posterior variance for $\mu$ based on the conjugate normal-normal model.
2. **MCMC Sampling & Posterior Estimation:** Implements a Metropolis-Hastings MCMC sampler to draw 100,000 samples from the posterior distribution of $\mu$. Use a normal proposal distribution centered at the current state with a standard deviation of 5.0. Start the chain at $\mu = 100.0$. Discard the first 10,000 samples as burn-in. Calculate the empirical mean and variance of the remaining MCMC samples.
3. **Statistical Hypothesis Comparison:** Using the remaining MCMC samples, calculate the empirical probability that the mean execution time $\mu > 105$ ms (i.e., the proportion of samples strictly greater than 105).

Compile and run your program to generate a report file at `/home/user/results.txt` with exactly the following format (floating point numbers printed to 4 decimal places):
```
Analytical Mean: [value]
Analytical Variance: [value]
MCMC Mean: [value]
MCMC Variance: [value]
P(mu > 105): [value]
```

To begin, you must first create the trace file `/home/user/trace.txt` with the following 10 execution times, one per line:
`106.5`
`103.2`
`108.1`
`104.5`
`107.8`
`102.1`
`109.3`
`105.4`
`106.9`
`108.2`

Write your C code, compile it using `gcc -O2 -lm analyze.c -o analyze`, and execute it to produce the `results.txt` file.