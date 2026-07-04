You are a data analyst working with a dataset of sensor measurements. We need to perform feature engineering, bootstrap sampling, and Bayesian inference to estimate the true difference between two redundant sensors.

Write and execute a C program to process the data and calculate the posterior mean of the difference between the sensors.

Here are the specific requirements:

1. **Environment & Input:**
   The input data is located at `/home/user/measurements.csv`. It contains two columns with a header: `SensorA` and `SensorB` (both are floating-point numbers). Read all rows (there will be $N$ data rows).

2. **Feature Engineering:**
   For each row, calculate a new feature $D$ representing the difference: $D = SensorA - SensorB$. 

3. **Bootstrap Sampling:**
   We want to estimate the mean of $D$ using bootstrap resampling. Generate $B = 10,000$ bootstrap samples. Each bootstrap sample must consist of $N$ draws with replacement from your calculated $D$ values.
   Compute the mean of each bootstrap sample, and then compute the grand mean ($\bar{D}_{boot}$) of these 10,000 bootstrap sample means.
   
   *Crucial: To ensure reproducible results across environments, do not use the standard C `rand()`. Instead, use the following Linear Congruential Generator (LCG) to select indices:*
   ```c
   unsigned long seed = 42;
   unsigned long my_rand() {
       seed = (1103515245 * seed + 12345) % 2147483648;
       return seed;
   }
   ```
   *To pick a random row index (0-indexed) for bootstrapping, use `my_rand() % N`.*

4. **Bayesian Inference:**
   Model the distribution of the true mean of $D$ using a Gaussian conjugate prior.
   - **Prior:** We assume a prior mean $\mu_0 = 0.0$ and prior variance $\sigma_0^2 = 1.0$.
   - **Likelihood:** We assume the data variance is known to be $\sigma^2 = 4.0$.
   - **Observations:** Treat $n = N$ (the original dataset size) as the number of observations, and $\bar{x} = \bar{D}_{boot}$ as the sample mean.
   
   Compute the posterior mean $\mu_n$ using the standard Normal-Normal conjugate update formula:
   $\mu_n = \frac{ \frac{1}{\sigma_0^2}\mu_0 + \frac{n}{\sigma^2}\bar{x} }{ \frac{1}{\sigma_0^2} + \frac{n}{\sigma^2} }$

5. **Output:**
   Write a C program (e.g., `/home/user/process.c`), compile it, and run it. 
   The program must save the final posterior mean $\mu_n$ into a text file located at `/home/user/posterior.txt`, formatted to exactly four decimal places (e.g., `1.2345`). Do not include any other text in this output file.