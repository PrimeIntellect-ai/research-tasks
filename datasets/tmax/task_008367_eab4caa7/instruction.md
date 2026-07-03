You are a data scientist analyzing a noisy periodic signal from a newly discovered physical phenomenon. The raw data is located at `/home/user/noisy_signal.csv`, containing two columns: `t` (time in seconds) and `y` (signal amplitude).

Your goal is to estimate the intrinsic physical parameter $A$ of the system and its uncertainty. According to the theoretical model, the signal is a sine wave where its time-domain amplitude $C$ is related to the intrinsic parameter $A$ by the nonlinear equation:
$A e^A = C$

Please perform the following steps and write a Python script to automate them:
1. **Spectral Analysis**: Load the dataset. Compute the Fast Fourier Transform (FFT) of `y` to find the dominant peak frequency $f_0$ (exclude the DC component, $f=0$).
2. **Amplitude Estimation**: The amplitude of the signal $C$ can be estimated from the FFT. Specifically, $C = P_{max} / (N/2)$, where $P_{max}$ is the magnitude of the FFT at the peak frequency $f_0$ and $N$ is the number of data points. Use a nonlinear root-finding method (e.g., `scipy.optimize.root_scalar`) to solve for the intrinsic parameter $A$.
3. **Monte Carlo Uncertainty Estimation**: To find the 95% confidence interval for $A$, perform a Monte Carlo simulation with exactly 1000 iterations. In each iteration $i$ (where $i$ ranges from 0 to 999):
   - Add synthetic Gaussian noise to the *original* raw signal `y`.
   - **Crucial for reproducibility:** For the $i$-th iteration, initialize your random number generator exactly as `rng = numpy.random.default_rng(42 + i)` and generate the noise array using `rng.normal(loc=0.0, scale=0.5, size=N)`. Add this noise to the original `y`.
   - Repeat the FFT analysis and nonlinear solving on this new noisy signal to get a new estimate for $A$.
4. **Parallelization**: The Monte Carlo simulation must be parallelized using Python's `multiprocessing` module (e.g., `multiprocessing.Pool`) across at least 4 CPU cores to speed up the computation.
5. **Output**: Calculate the 2.5th and 97.5th percentiles of the 1000 simulated $A$ values to serve as the lower and upper bounds of the confidence interval.

Save your final results in a JSON file at `/home/user/model_fit.json` with the following exact keys:
- `"f0"`: The estimated peak frequency (float).
- `"A_estimate"`: The initial estimate of $A$ from the original raw data (float).
- `"A_ci_lower"`: The 2.5th percentile of $A$ from the Monte Carlo simulation (float).
- `"A_ci_upper"`: The 97.5th percentile of $A$ from the Monte Carlo simulation (float).

Round all values in the JSON file to exactly 3 decimal places.