You are a performance engineer tasked with optimizing and analyzing a Markov Chain Monte Carlo (MCMC) simulation written in C. 

The application `/home/user/mcmc.c` implements a Metropolis-Hastings algorithm to estimate the posterior distribution of the mean (`mu`) and standard deviation (`sigma`) of a dataset located at `/home/user/data.txt`. 

Currently, the C code is functionally correct but contains a severe performance bottleneck making it run extremely slowly. Your tasks are as follows:

1. **Optimize the C code**: Identify and fix the severe performance bottleneck in `/home/user/mcmc.c`. The fixed code should use the same Metropolis-Hastings logic and random number generation sequence but execute in a fraction of the time. (Do not change the random seed or the custom random number generator).
2. **Compile and Run**: Compile your optimized code into `/home/user/mcmc_opt` (using `gcc`). Run it to generate a trace file of the MCMC samples at `/home/user/trace.csv`. The C program is already configured to write `mu,sigma` to standard output. Redirect this to the CSV file (it will print 10,000 lines).
3. **Statistical Analysis**: Calculate the expected value (mean) of the posterior samples for both `mu` and `sigma` based on the data in `trace.csv`. 
   - You must discard the first 1,000 samples as "burn-in".
   - Compute the mean of the remaining 9,000 samples for both parameters.
   - Write the final results to `/home/user/results.txt` exactly in this format:
     ```
     mu=X.XX
     sigma=Y.YY
     ```
     (Round to two decimal places).
4. **Visualization**: Create a Python script to visualize the MCMC experimental data. Plot a 2D scatter plot of the post-burn-in samples (X-axis: `mu`, Y-axis: `sigma`). Save the plot as `/home/user/trace_plot.png`.

Ensure all files (`mcmc_opt`, `trace.csv`, `results.txt`, `trace_plot.png`) are located precisely in `/home/user/`.