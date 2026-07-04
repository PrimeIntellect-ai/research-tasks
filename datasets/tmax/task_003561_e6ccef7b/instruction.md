You are a researcher running simulations to identify an unknown material based on its vibrational frequency. 

Please perform the following steps to process the simulated data and identify the material:

1. **Monte Carlo Simulation**: Write a script (in any language you prefer, such as Python) to generate 500 independent realizations of a noisy time-domain signal.
   - The base signal is $y(t) = 3.0 \sin(2 \pi f_{true} t)$
   - $f_{true} = 18.23$ Hz.
   - Time $t$ consists of 1000 equally spaced points from $0$ up to $10$ seconds (excluding 10, e.g., using `numpy.linspace(0, 10, 1000, endpoint=False)` or equivalent, so the sampling interval $dt = 0.01$ s).
   - Add random Gaussian noise to each realization with a mean of 0 and a standard deviation of 5.0.

2. **Spectral Analysis**: For each of the 500 realizations, compute the power spectrum. The power spectrum is defined as the squared magnitude of the discrete Fourier transform. Average the 500 power spectra together to get a stable averaged power spectrum. (If using Python, use `numpy.fft.rfft` and `numpy.fft.rfftfreq` with `d=0.01`).

3. **Curve Fitting**: Find the frequency bin in the averaged power spectrum that contains the maximum power. Let this peak frequency be $f_p$. Select this point and its two immediate neighbors, $f_{p-1}$ and $f_{p+1}$. Fit a quadratic polynomial (parabola) $P(f) = a f^2 + b f + c$ to these three data points to estimate the precise true peak frequency, given by the vertex of the parabola: $f_{peak} = -b / (2a)$.

4. **Reference Comparison**: Read the file `/home/user/references.csv`, which contains a list of known materials and their theoretical frequencies. Find the material whose frequency is closest to your estimated $f_{peak}$ in absolute value.

5. **Output**: Write the identified material name and your estimated $f_{peak}$ (rounded to two decimal places) to `/home/user/result.txt`, formatted exactly as:
   `MaterialName, 18.XX`