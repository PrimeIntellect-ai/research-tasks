You are a Machine Learning Engineer preparing a synthetic time-series dataset for training. You need to write a Python script that generates this data, optimizes its spectral properties, and calculates statistically stable metrics. We have noticed non-reproducible results in our pipelines due to floating-point reduction order variations across different architectures, so you must be extremely precise with how you accumulate values.

Create a workspace at `/home/user/workspace`. Set up a Python virtual environment named `venv` in this directory and install any necessary scientific packages (`numpy`, `scipy`).

Write a script at `/home/user/workspace/prepare_data.py` that performs the following steps:

1. **Signal Optimization (Spectral Analysis & Optimization)**
   We need to find the optimal coefficients $(c_1, c_2, c_3)$ for a base signal $x(t) = c_1 \sin(2\pi \cdot 5 t) + c_2 \sin(2\pi \cdot 15 t) + c_3 \sin(2\pi \cdot 30 t)$.
   - The signal is sampled at $f_s = 100$ Hz for $1$ second ($N=100$ samples), so $t = 0, 0.01, \dots, 0.99$.
   - The signal passes through a non-linear distortion: $y(t) = \tanh(x(t))$.
   - Use `scipy.optimize.minimize` with the `Nelder-Mead` method to find $[c_1, c_2, c_3]$ that minimizes the Sum of Squared Errors (SSE) between the single-sided FFT amplitude peaks of $y(t)$ at 5Hz, 15Hz, and 30Hz, and the target amplitudes $[2.0, 1.0, 0.5]$.
   - Note: For a 100-point FFT, the single-sided amplitude at bin $k$ ($0 < k < 50$) is given by `(2 / N) * abs(fft_result[k])`.
   - Use an initial guess of `[1.0, 1.0, 1.0]`.

2. **Data Generation & Exact Reduction**
   - Using the optimized coefficients, generate 1000 noisy variants of $y(t)$.
   - For variant $i$, $y_i(t) = \tanh(x(t)) + \epsilon_i(t)$, where $\epsilon_i(t) \sim \mathcal{N}(0, 0.1^2)$.
   - Initialize your noise generator exactly once using `rng = numpy.random.default_rng(42)` and generate all noise as a single `(1000, 100)` matrix.
   - For each of the 1000 variants, compute the "Signal Energy" (the sum of the squared values of the variant's 100 samples). 
   - *CRITICAL:* To prevent floating-point reduction order issues, you must calculate this sum using Python's standard `math.fsum()` on the squared values (convert the numpy array of squared values to a python list/iterable first).

3. **Bootstrap Confidence Intervals**
   - We need the 95% confidence interval for the *mean* Signal Energy across the 1000 variants.
   - Use a custom bootstrap: initialize a new generator `rng_boot = numpy.random.default_rng(99)`.
   - Draw 5000 bootstrap samples (each of size 1000, with replacement) from your 1000 computed energies. Do this by generating a single index matrix `rng_boot.choice(1000, size=(5000, 1000), replace=True)`.
   - Calculate the mean of each bootstrap sample.
   - Calculate the 2.5th and 97.5th percentiles of these 5000 means using `numpy.percentile` to get `[ci_lower, ci_upper]`.

4. **Output**
   - Save a JSON file at `/home/user/workspace/results.json` containing the optimized coefficients and confidence intervals.
   - Format:
     ```json
     {
       "c1": float,
       "c2": float,
       "c3": float,
       "energy_ci_lower": float,
       "energy_ci_upper": float
     }
     ```

Run your script to produce `results.json`.