I am preparing training data for a machine learning model that predicts physical system properties. As a first step, I need to generate baseline data for a custom 1D target probability density function, $f(x)$, and verify our sampling method against numerical integration.

The unnormalized target density is:
$f(x) = \exp(-x^2/2) \cdot (1 + \sin(2x)^2)$

Please perform the following steps:

1. Write a C++ program named `/home/user/data_prep.cpp` that does the following:
   - **Numerical Integration:** Use the Trapezoidal rule with $N=10000$ intervals over the domain $x \in [-10, 10]$ to approximate the normalization constant $Z = \int_{-10}^{10} f(x) dx$ and the second moment $I_2 = \int_{-10}^{10} x^2 f(x) dx$. Compute the exact expected variance $V_{exact} = I_2 / Z$.
   - **MCMC Sampling:** Implement a Metropolis-Hastings sampler to draw samples from $f(x)$. 
     - Use a Gaussian proposal distribution $Q(x'|x) \sim \mathcal{N}(x, \sigma^2=1.0)$.
     - Start at $x_0 = 0.0$.
     - Run the sampler for 100,000 iterations.
     - Discard the first 10,000 samples as burn-in.
   - **Posterior Estimation:** Calculate the sample variance $V_{mcmc}$ of the remaining 90,000 samples.
   - **Output 1:** Save all 90,000 post-burn-in samples to `/home/user/samples.csv` (one float per line).
   - **Output 2:** Write the calculated variances to `/home/user/results.txt` in exactly this format:
     ```
     Exact: <V_exact>
     MCMC: <V_mcmc>
     ```

2. Compile and run the C++ program. Use `-O3` for optimization.

3. Experimental Data Visualization: Write a Python script `/home/user/plot_samples.py` that reads `/home/user/samples.csv` and uses `matplotlib` to plot a 50-bin histogram of the samples. Save the plot to `/home/user/histogram.png`. Run the script to generate the image (you may need to install `matplotlib` locally via pip if it's not present).

Complete the task by ensuring all files (`data_prep.cpp`, `samples.csv`, `results.txt`, `plot_samples.py`, and `histogram.png`) are correctly generated in `/home/user`.