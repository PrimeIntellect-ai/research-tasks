You are a machine learning engineer preparing synthetic training data. We need to generate a synthetic dataset that mimics the distribution of a reference dataset, and then verify its density distribution.

You are provided with a reference dataset at `/home/user/ref_data.txt`, which contains a single column of numerical values.

Perform the following steps using strictly standard Linux CLI tools (Bash, awk, sort, etc.):

1. **Calculate Reference Statistics:**
   Read `/home/user/ref_data.txt` and calculate its mean ($\mu$) and sample standard deviation ($\sigma$). Use the standard sample standard deviation formula (dividing by $N-1$).

2. **MCMC Sampling (Metropolis Algorithm):**
   Generate 10,000 samples from a Normal distribution $\mathcal{N}(\mu, \sigma^2)$ using the Metropolis algorithm in `awk`.
   - Set the random seed to 42 exactly once in the `BEGIN` block: `srand(42)`.
   - Set the initial state to $x = \mu$.
   - For exactly 10,000 iterations, do the following in order:
     1. Output the current state $x$ (so the first output is exactly $\mu$).
     2. Generate a proposed state: $x_{prop} = x + (rand() - 0.5) \times 4 \times \sigma$.
     3. Calculate the acceptance probability ratio $\alpha = \frac{P(x_{prop})}{P(x)}$, where $P(v) = \exp\left( -\frac{(v-\mu)^2}{2\sigma^2} \right)$.
     4. If $\alpha \ge 1$, accept the proposal ($x = x_{prop}$).
     5. If $\alpha < 1$, generate a uniform random number $u = rand()$. If $u < \alpha$, accept the proposal ($x = x_{prop}$). Otherwise, reject it ($x$ remains unchanged).
   - Save the 10,000 generated values to `/home/user/synthetic_data.txt` (one value per line).

3. **Density Estimation (Histogram):**
   Create a histogram of the values in `/home/user/synthetic_data.txt` to estimate the empirical density.
   - Define 10 equal-width bins covering the range $[\mu - 3\sigma, \mu + 3\sigma)$.
   - The width of each bin is $w = \frac{6\sigma}{10}$.
   - A value $v$ falls into bin index $k = \lfloor \frac{v - (\mu - 3\sigma)}{w} \rfloor$.
   - Count the number of samples that fall into each bin $k \in \{0, 1, 2, ..., 9\}$. Ignore any samples that fall outside the overall range (i.e., $k < 0$ or $k \ge 10$).
   - Write the counts to `/home/user/histogram.txt`, one count per line, from bin 0 to bin 9. The file should contain exactly 10 lines with integer counts.