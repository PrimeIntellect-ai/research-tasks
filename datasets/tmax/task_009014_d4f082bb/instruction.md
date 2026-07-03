You are an AI assistant acting as a data scientist analyzing a noisy, spatially uneven sensor signal. 

Your objective is to build a C++ pipeline that standardizes the spatial domain (mesh regularization), extracts the dominant frequency via Spectral Analysis, and estimates the amplitude and phase of the signal using Markov Chain Monte Carlo (MCMC).

**Background:**
You have been provided with a dataset at `/home/user/raw_signal.csv`. The file has two comma-separated columns: `x` (spatial coordinate, sorted in ascending order but unevenly spaced) and `y` (signal value).
The underlying signal is assumed to be modeled as:
$$y(x) = A \sin(2 \pi f x + \phi) + \epsilon$$
where $\epsilon \sim \mathcal{N}(0, \sigma^2)$ with known $\sigma = 0.5$.

**Pipeline Requirements:**

1. **Environment Setup:**
   Install any necessary C++ libraries for Fourier transforms (e.g., FFTW3). You have `sudo` privileges to install apt packages if needed.

2. **Mesh Regularization:**
   Write a C++ program (e.g., `fit_model.cpp`) that reads `/home/user/raw_signal.csv`.
   Create a uniform spatial mesh of exactly $N = 1024$ points, starting at $x_{min}$ (the first $x$ value in the data) and ending at $x_{max}$ (the last $x$ value).
   Interpolate the $y$ values onto this uniform mesh using standard linear interpolation.

3. **Spectral Analysis:**
   Compute the Discrete Fourier Transform (DFT) of the uniform mesh $y$ values.
   Find the dominant frequency $f_{est}$. Ignore the DC component (index 0). The frequency corresponding to DFT bin index $k$ (for $k < N/2$) is $f_k = \frac{k}{x_{max} - x_{min}}$.
   Let $f = f_{est}$ be fixed for the next step.

4. **MCMC Posterior Estimation:**
   Implement a Metropolis-Hastings MCMC sampler in your C++ code to estimate the posterior means of $A$ and $\phi$.
   - **Priors:** Assume uniform priors: $A \sim U(0, 5)$ and $\phi \sim U(0, 2\pi)$.
   - **Likelihood:** Use the Gaussian likelihood over the *original uneven dataset* (not the interpolated mesh), using the fixed $f_{est}$ and $\sigma = 0.5$.
   - **Proposal Distribution:** Gaussian centered at the current value, with standard deviation $0.1$ for both $A$ and $\phi$. Boundary reflections or rejections outside the prior bounds should be handled.
   - **Initialization:** $A = 1.0, \phi = 0.0$.
   - **Randomness:** Use `std::mt19937` seeded with `42` for reproducibility.
   - **Iterations:** Run for exactly $10,000$ iterations. Discard the first $2,000$ as burn-in. Calculate the mean of $A$ and $\phi$ over the remaining $8,000$ samples.

5. **Output Generation:**
   Compile and run your code. Your C++ program must write its final results to `/home/user/fit_results.txt` in the following exact format:
   ```
   f_est: <float>
   A_mean: <float>
   phi_mean: <float>
   ```
   Provide the floats to at least 4 decimal places.