A previous data scientist left behind a project simulating an underdamped noisy oscillator, but the numerical integrator diverges or produces highly inaccurate frequency spectra due to poor step-size adaptation. 

Your goals are:
1. Inspect the image `/app/reference_spectrum.png` to determine the target natural frequency (`f0`) and damping coefficient (`Gamma`) of the system. The exact values are written in the plot title.
2. Fix the C simulation code in `/app/simulator.c`. It currently uses a simple Euler method with a hardcoded time step (`dt`) that is far too large, causing instability and frequency aliasing. Reduce the time step to `0.01` or smaller, and proportionally increase the number of steps so the total simulation time remains exactly 200 seconds. Compile it to `/app/simulator`.
3. The simulator takes three arguments: `./simulator <f0> <Gamma> <random_seed>`. Run a Monte Carlo simulation of 100 independent trials using seeds 1 through 100, using the `f0` and `Gamma` you extracted from the image.
4. For each trial's time-series output, compute the Power Spectral Density (using a Fourier Transform/FFT) and identify the peak frequency (the frequency with the maximum power, ignoring the DC component at 0 Hz).
5. Perform a bootstrap analysis (with at least 1000 resamples) on the 100 peak frequencies to compute the 95% confidence interval for the mean peak frequency.
6. Save your results in `/app/metrics.json` strictly using the following format:
```json
{
  "mean": 4.123,
  "ci_lower": 4.100,
  "ci_upper": 4.150
}
```

Make sure your environment has the necessary tools installed (you may need to install FFT or bootstrap libraries if using Python, or use standard ones like `numpy` and `scipy`).