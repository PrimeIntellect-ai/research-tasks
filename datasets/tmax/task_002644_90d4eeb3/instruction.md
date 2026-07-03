You are a data scientist analyzing a chaotic system under noisy forcing. Your objective is to determine the dominant frequency of a Duffing oscillator subject to random driving amplitudes using Monte Carlo simulation and spectral analysis.

Write a Python script at `/home/user/duffing_mc.py` that performs the following steps:
1. Set the NumPy random seed to `42`.
2. Simulate a Duffing oscillator described by the following system of ODEs:
   $dx/dt = v$
   $dv/dt = -0.1 v - x - x^3 + A \cos(1.2 t)$
3. Run $N=100$ independent Monte Carlo trials. For each trial, draw the driving amplitude $A$ from a normal distribution with mean $2.0$ and standard deviation $0.5$.
4. For each trial, integrate the system from $t=0$ to $t=50$ using `scipy.integrate.solve_ivp` with the `RK45` method. Initial conditions are $x(0)=0, v(0)=0$. Use `t_eval` to evaluate the solution at exactly 1000 evenly spaced points from $0$ to $50$ inclusive.
5. For each trial, calculate the power spectrum of the $x(t)$ time series. The power spectrum is defined as the squared magnitude of the discrete Fourier transform (DFT) of $x(t)$.
6. Average the power spectra across all 100 trials.
7. Find the positive frequency $f > 0$ (in Hz, or cycles per unit time) that corresponds to the maximum power in the averaged spectrum.
8. Round this dominant frequency to 3 decimal places and write it to a text file at `/home/user/dominant_freq.txt`.

You must install any necessary Python packages (like `numpy`, `scipy`) using `pip` if they are not already installed.