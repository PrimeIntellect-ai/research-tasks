You are a machine learning engineer tasked with generating robust, denoised synthetic training data based on a physical system's dynamics, and estimating the underlying physical parameters along with their statistical confidence intervals. 

Your goal is to write and execute a Python script that generates this data, denoises it using matrix decomposition, performs numerical optimization to find the system parameters, and uses bootstrapping to find confidence intervals.

Please complete the following steps:

1. **Environment Setup**:
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `numpy` and `scipy`.
   - Create a directory `/home/user/ml_data`.

2. **Data Generation** (ODE Integration):
   - The physical system is a damped harmonic oscillator described by the ODE: 
     $x''(t) + \gamma x'(t) + \omega^2 x(t) = 0$
   - Generate true trajectories for 10 different initial conditions: 
     $x(0) \in \{1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9\}$, and $x'(0) = 0$.
   - Use true parameters: $\gamma = 0.5$, $\omega = 2.0$.
   - Integrate over $t \in [0, 10]$ with exactly 100 points (using `numpy.linspace(0, 10, 100)`).
   - Construct a matrix `X_true` of shape `(100, 10)` where each column is the time series $x(t)$ for one initial condition.
   - Add Gaussian noise to create `X_noisy`: Set `numpy.random.seed(42)` immediately before generating the noise. The noise should be drawn from a normal distribution $\mathcal{N}(\mu=0, \sigma=0.1)$ of the same shape as `X_true`. `X_noisy = X_true + noise`.

3. **Denoising** (Matrix Decomposition):
   - Perform Singular Value Decomposition (SVD) on `X_noisy`.
   - Reconstruct the matrix using only the top 2 singular values/vectors. Let this be `X_denoised`.

4. **Parameter Estimation** (Optimization):
   - Define an objective function that takes parameters $[\gamma, \omega]$, integrates the ODE for all 10 initial conditions, and computes the Mean Squared Error (MSE) between the resulting `X_simulated` and `X_denoised` over all elements.
   - Use `scipy.optimize.minimize` with the Nelder-Mead method to find the best-fit parameters $\gamma_{fit}$ and $\omega_{fit}$. 
   - Use initial guess: $\gamma = 0.2, \omega = 1.5$.

5. **Bootstrap Confidence Intervals**:
   - Calculate the residuals: `R = X_denoised - X_fit` (where `X_fit` is simulated using $\gamma_{fit}$ and $\omega_{fit}$).
   - Perform 100 bootstrap iterations to find confidence intervals for $\gamma$ and $\omega$.
   - **Crucial**: Set `numpy.random.seed(42)` exactly once immediately *before* the loop of 100 iterations.
   - In each iteration:
     a. Resample the residuals by drawing with replacement from the flattened `R` to create `R_boot` of shape `(100, 10)`.
     b. Create bootstrapped data: `X_boot = X_fit + R_boot`.
     c. Optimize to find new parameters $[\gamma^*, \omega^*]$ fitting `X_boot`, using $[\gamma_{fit}, \omega_{fit}]$ as the initial guess. Use Nelder-Mead.
   - Calculate the 2.5th and 97.5th percentiles (using `numpy.percentile`) for both $\gamma^*$ and $\omega^*$.

6. **Output**:
   - Save the results to `/home/user/ml_data/results.txt` with exactly the following format (round all numbers to 4 decimal places):
     ```
     gamma: <value>
     omega: <value>
     gamma_ci: [<low>, <high>]
     omega_ci: [<low>, <high>]
     ```

Run your code and ensure the output file is generated correctly.