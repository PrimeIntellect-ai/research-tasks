You are a bioinformatics analyst tasked with estimating the degradation rate parameter ($\theta$) of ancient DNA sequences over time using a Bayesian framework.

You have been given a C program, `/home/user/mcmc_degrade.c`, which uses a Metropolis-Hastings MCMC algorithm to sample the posterior distribution of $\theta$. The likelihood is calculated by simulating the sequence degradation ODE: $dy/dt = -\theta y$, starting from $y(0) = 100$. We have an observation $y(10) = 4.9787$.

However, there is a problem. The analytical expected value for $\theta$ is approximately $0.300$ (since $100 e^{-10 \times 0.3} \approx 4.9787$). But the provided C code yields divergent behavior or completely incorrect posterior distributions. This is because the numerical integrator inside the log-likelihood function uses a hardcoded, overly large step size (`dt = 2.0`), which causes the Euler method to oscillate or diverge for certain proposal values of $\theta$.

Your tasks are to:
1. Fix the numerical integrator in `/home/user/mcmc_degrade.c` by reducing the step size `dt` to `0.01` (ensure the loop bounds are adjusted so it still integrates from $t=0$ to $t=10$).
2. Write a pure Bash orchestration script at `/home/user/run_pipeline.sh` that:
   - Compiles the fixed C program using `gcc -O2 mcmc_degrade.c -o mcmc_run -lm`.
   - Runs three separate MCMC chains using the compiled executable with random seeds `10`, `20`, and `30` (the C program accepts the seed as a single command-line argument: `./mcmc_run <seed>`).
   - The C program prints one sampled $\theta$ value per line (totaling 5500 lines per run).
   - For each chain, discard the first 500 lines as burn-in.
   - Aggregate the remaining 5000 lines from all three chains (15000 samples total) and calculate the global posterior mean of $\theta$.
   - Save ONLY this final mean value, formatted to exactly 3 decimal places, to `/home/user/posterior_mean.txt`.

Ensure your bash script uses standard CLI tools (`awk`, `sed`, `tail`, `cat`, etc.) to process the results and orchestrate the pipeline. Do not use Python or other scripting languages for the pipeline.