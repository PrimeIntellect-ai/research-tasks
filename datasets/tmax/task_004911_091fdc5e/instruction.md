You are a machine learning engineer preparing a synthetic dataset of physical signals for training a new neural network. The signals represent damped harmonic oscillators, but you've previously had issues with numerical integrators diverging or producing artifacts due to improper step-size adaptation.

Create a Python script at `/home/user/prepare_dataset.py` that generates the data and computes specific statistics to verify the integrity of the dataset. 

Your script must perform the following steps:
1. **Analytical Validation (Convergence Testing)**: 
   Consider the damped harmonic oscillator: $y'' + 0.1 y' + \omega^2 y = 0$, with initial conditions $y(0) = 1, y'(0) = 0$. 
   First, validate your numerical solver for $\omega = 5.0$. Simulate from $t = 0$ to $t = 100$ using `scipy.integrate.solve_ivp` (evaluate at 1000 evenly spaced points from 0 to 100 inclusive). Use tight tolerances (`rtol=1e-6`, `atol=1e-8`) to prevent divergence.
   Compare the numerical $y(t)$ to the exact analytical solution for this underdamped case. Compute the maximum absolute error over the 1000 points.

2. **Dataset Generation**:
   Set the random seed using `numpy.random.seed(42)`. Sample 50 values for $\omega$ from a uniform distribution $\mathcal{U}(2, 8)$.
   For each $\omega$, simulate the oscillator over $t \in [0, 100]$ (1000 evenly spaced points) using the same solver settings.

3. **Spectral Analysis**:
   For each of the 50 generated signals $y(t)$, compute the Fast Fourier Transform (FFT) to find the power spectrum. Identify the dominant frequency (the positive frequency component with the highest magnitude). Keep track of these 50 dominant frequencies. *(Hint: remember the relationship between angular frequency $\omega$ and standard frequency $f$ when using FFT tools, though here we want you to report the dominant standard frequency $f$ in Hz, where $f = \omega / 2\pi$)*.

4. **Density Estimation**:
   Perform a Gaussian Kernel Density Estimation (KDE) on the 50 extracted dominant frequencies using `scipy.stats.gaussian_kde` with its default bandwidth selection. Evaluate the estimated Probability Density Function (PDF) at the frequency corresponding to $\omega = 5.0$ (which is $f = 5.0 / 2\pi$).

Finally, your script must output a JSON file at `/home/user/dataset_stats.json` with exactly the following keys:
- `"max_error_validation"`: The maximum absolute error from the analytical validation step (float).
- `"mean_dominant_freq"`: The mean of the 50 dominant frequencies in Hz (float).
- `"kde_at_target"`: The evaluated KDE PDF value at $f = 5.0 / 2\pi$ (float).

Run your script to produce the output file.