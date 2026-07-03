You are acting as a data scientist working on fitting a model to time-resolved spectroscopy data. 

In `/home/user`, there is a file called `spectroscopy_data.csv` containing two columns: `time` and `signal`. This data represents the oscillations of a coherent phonon.

You have a starter script, `/home/user/fit_phonon.py`, which attempts to find the best damping constant (`gamma`) and angular frequency (`omega`) for a damped harmonic oscillator model:
d²x/dt² + 2*gamma*(dx/dt) + omega²*x = 0
with initial conditions x(0) = 1.0, dx/dt(0) = 0.0.

Currently, the script is failing to find a good fit. It suffers from three major issues:
1. **Divergent Integrator:** The forward model uses a fixed-step Euler integrator with a hardcoded step size that diverges for high-frequency parameters during the search, resulting in NaNs. 
2. **Inappropriate Cost Function:** The time-domain Mean Squared Error is highly sensitive to slight phase shifts. You need to change the cost function to compare the power spectra of the signals.
3. **Missing Monte Carlo Search:** The parameter search loop is incomplete.

Your task:
1. Fix the numerical integration in `fit_phonon.py`. Replace the buggy Euler integrator with `scipy.integrate.solve_ivp` (or similar adaptive solver) to ensure convergence across the entire parameter space. Evaluate the solution at the exact time points given in `spectroscopy_data.csv`.
2. Implement a new cost function: compute the Real Fast Fourier Transform (`np.fft.rfft`) of both the simulated signal and the experimental signal. The cost should be the Sum of Squared Differences between their **magnitudes** (absolute values of the FFT).
3. Implement a Monte Carlo random search to find the best parameters. 
    - Set the numpy random seed to `42` (`np.random.seed(42)`) immediately before the loop.
    - Draw 2000 uniform random samples for `gamma` in the range `[0.1, 2.0]`.
    - Draw 2000 uniform random samples for `omega` in the range `[5.0, 10.0]`.
    - Evaluate the FFT-based cost for each pair.
4. Save the parameters that produced the minimum cost to a JSON file at `/home/user/best_params.json` with the format: `{"gamma": float, "omega": float}`.

Ensure your code handles the data ingestion properly and that the final JSON file is strictly formatted.