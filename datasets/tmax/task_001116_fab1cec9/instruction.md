You are a data scientist modeling a synthetic biological oscillator. The system is modeled as a Van der Pol oscillator, but the custom adaptive ODE solver you've been given is producing divergent, high-frequency garbage due to a bug in its step-size adaptation logic. 

Your goal is to fix the integrator, process the resulting time series, and fit a model parameter using spectral analysis and a nonlinear root finder.

**Step 1: Fix the ODE Integrator**
A script is located at `/home/user/simulate.py`. It contains a function `adaptive_euler_heun(mu)` that integrates the system using an embedded Heun-Euler method. 
*   **The Bug:** The local truncation error calculation is wrong (`error = np.sum(y_h - y_e)`). If errors cancel out, the step size artificially inflates, causing instability.
*   **The Fix:** Modify `/home/user/simulate.py` so that `error` is calculated as the **maximum absolute difference** between the Heun and Euler steps across all state variables.

**Step 2: Resampling and Spectral Analysis**
The corrected integrator will output non-uniformly sampled points `(times, states)`. Write a new script, `/home/user/fit_mu.py`, that does the following:
*   Imports the corrected `adaptive_euler_heun` function.
*   Runs the simulation for a given $\mu$.
*   Takes the first state variable ($y_1$) and interpolates it onto a strictly uniform grid from $t = 100.0$ to $t = 600.0$ (inclusive) with a time step of $\Delta t = 0.1$. (Use `scipy.interpolate.interp1d` with `kind='linear'`).
*   Computes the real Fast Fourier Transform (`np.fft.rfft`) of this uniformly sampled $y_1$ segment (do not apply any windowing).
*   Determines the **dominant frequency** (in Hz) corresponding to the peak magnitude of the FFT (ignoring the DC component at $f=0$).

**Step 3: Nonlinear Parameter Fitting**
The oscillator's frequency depends on the parameter $\mu$. 
*   Using your spectral analysis pipeline, define an objective function `f(mu) = dominant_frequency(mu) - 0.140`.
*   Use a nonlinear root-finding algorithm (e.g., `scipy.optimize.brentq`) to find the value of $\mu$ in the interval `[1.0, 2.0]` that makes the dominant frequency exactly $0.140$ Hz.
*   Save the final fitted value of $\mu$ to `/home/user/mu_solution.txt`, rounded to exactly 3 decimal places (e.g., `1.234`).

**Requirements:**
*   You must use Python.
*   The system has standard scientific libraries installed (`numpy`, `scipy`).
*   Ensure your final script cleanly outputs the result to `/home/user/mu_solution.txt`.