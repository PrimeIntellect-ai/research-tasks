You are a Machine Learning Engineer preparing training data for a surrogate model. You are using a C program that performs Markov Chain Monte Carlo (MCMC) sampling to find the posterior mean of the parameters for a linear regression model ($y = mx + c$). 

However, the current implementation in `/home/user/mcmc_fit.c` produces non-reproducible and wildly inaccurate results. The dataset (`/home/user/data.csv`) contains 1,000,000 data points. To simulate memory constraints on the target edge device, the data arrays are strictly typed as `float`. The likelihood function calculates the Sum of Squared Errors (SSE) using a naive loop. Because of the large number of data points, catastrophic cancellation and floating-point accumulation errors destroy the precision of the SSE calculation, which ruins the MCMC acceptance ratios.

Your task:
1. Identify the `compute_sse` function in `/home/user/mcmc_fit.c`.
2. Fix the numerical stability issue by implementing **Kahan summation** for the SSE reduction. 
   *Constraint:* You must NOT change the data types of the arrays or the function signature (it must still return a `float` and take `float*` arrays). You must implement the Kahan summation algorithm to preserve precision during the loop.
3. Compile the fixed C program: `gcc -O2 -o mcmc_fit mcmc_fit.c -lm`
4. Run the program. It will output the posterior mean for `m` and `c` after processing the data.
5. Create a file at `/home/user/posterior.txt` containing exactly the final estimated parameters in the following format:
   `m=<value>,c=<value>`
   (Replace `<value>` with the exact outputs from your fixed program, to 4 decimal places, e.g., `m=3.1415,c=2.7182`).