You are assisting a physics researcher in validating a numerical simulation of a diffusion process against an analytical solution derived via Fourier analysis. 

The process is a 1D random walk where each step is drawn from a uniform distribution $\mathcal{U}(-\sqrt{3}, \sqrt{3})$ (which has a mean of 0 and a variance of 1). 

Please write a Python script at `/home/user/analyze_diffusion.py` that performs the following steps:

1. **Simulation and Density Estimation**:
   - Set the random seed to `42` using `numpy.random.seed(42)`.
   - Simulate $M = 100,000$ independent particles, each taking $N = 100$ steps.
   - Calculate the final position of each particle.
   - Fit a Gaussian Kernel Density Estimator (KDE) to the final positions using `scipy.stats.gaussian_kde` with the default bandwidth selection (Scott's rule).

2. **Analytical Solution via Fourier Transform**:
   - The characteristic function of a single step is $\phi(k) = \frac{\sin(\sqrt{3}k)}{\sqrt{3}k}$ (with $\phi(0)=1$).
   - The characteristic function of the final position after $N$ steps is $\Phi(k) = \phi(k)^N$.
   - Compute the analytical Probability Density Function (PDF) using the discrete inverse Fourier transform (`numpy.fft.ifft`).
   - Use a spatial grid $x \in [-L, L)$ where $L = 100$ and the number of grid points is $N_{grid} = 4096$. The spacing is $dx = 2L / N_{grid}$.
   - The corresponding angular frequencies $k$ can be found using $k = 2\pi \cdot \text{fftfreq}(N_{grid}, dx)$.
   - Evaluate $\Phi(k)$ on this grid, apply the inverse FFT, and correctly shift and scale the result to obtain the analytical PDF $p_{analytical}(x)$. (Hint: ensure the integral of the PDF is 1).

3. **Validation**:
   - Evaluate both the empirical KDE and the analytical PDF at the specific evaluation points: $X_{eval} = [-10.0, -5.0, 0.0, 5.0, 10.0]$. 
   - For the analytical PDF, you may linearly interpolate the values from your FFT spatial grid to the evaluation points.
   - Compute the maximum absolute difference between the KDE values and the analytical values at these 5 points.

4. **Output**:
   - The script must save a JSON file at `/home/user/diffusion_metrics.json` with the following structure:
     ```json
     {
       "kde_values": [val1, val2, val3, val4, val5],
       "analytical_values": [val1, val2, val3, val4, val5],
       "max_diff": float
     }
     ```
   - All arrays should be standard lists of Python floats.

You can install any required Python packages (like `numpy`, `scipy`) using `pip`. Execute your script to generate the JSON file.