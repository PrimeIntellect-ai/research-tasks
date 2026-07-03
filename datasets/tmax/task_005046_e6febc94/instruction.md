I am an ML engineer preparing a dataset of physical system responses for training a surrogate model. Our pipeline involves taking noisy amplitude measurements, simulating a driven damped harmonic oscillator, and extracting the peak spectral response. 

We have a scanned specification sheet located at `/app/config_spec.png` which contains the natural frequency (`w0`) and the numerical integration time step (`dt`) of the system.

Please create a reproducible Python pipeline script at `/home/user/process_signal.py` that does the following:

1. **Input parsing:** Read a single line from standard input (`stdin`). This line will contain a comma-separated list of float values (noisy amplitude measurements).
2. **Density estimation:** Fit a Gaussian Kernel Density Estimate (KDE) to these measurements using `scipy.stats.gaussian_kde` (with default parameters/bandwidth). Evaluate the KDE at exactly 200 linearly spaced points from `-10.0` to `10.0` (inclusive, using `numpy.linspace(-10.0, 10.0, 200)`). Find the maximum density value among these evaluated points. Let this maximum density value be $A$ (the estimated true amplitude).
3. **Parameter extraction:** Read the image `/app/config_spec.png` (using OCR, e.g., pytesseract) to extract the values of `w0` and `dt`. The image contains text roughly like `w0 = [value]` and `dt = [value]`.
4. **ODE Numerical Solving:** Simulate a driven damped harmonic oscillator using the Forward Euler method. The system is defined by:
   $y_{n+1} = y_n + dt \cdot v_n$
   $v_{n+1} = v_n + dt \cdot (A \sin(2.0 \cdot t_n) - 0.1 \cdot v_n - w_0^2 \cdot y_n)$
   
   - Start with initial conditions $y_0 = 0.0$ and $v_0 = 0.0$.
   - Run the simulation for exactly 200 steps (i.e., `n` goes from `0` to `199`), where $t_n = n \cdot dt$.
   - Store the $y_{n+1}$ values at each step into a list (this list should have 200 elements).
5. **Spectral analysis:** Apply a 1D Discrete Fourier Transform to the 200-element list of $y$ values using `numpy.fft.fft`.
6. **Output:** Compute the absolute magnitude of the FFT results. Find the maximum magnitude, round it to exactly 4 decimal places, and print it to standard output (`stdout`).

Ensure your script is executable and robust. We will test it against a reference implementation with various randomized input streams to guarantee exact numerical equivalence.