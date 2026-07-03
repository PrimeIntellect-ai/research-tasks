You are a data scientist tasked with analyzing noisy, irregularly sampled displacement data from a mechanical sensor. The system is a driven damped harmonic oscillator, but the exact system parameters are unknown.

The raw data is located at `/home/user/data/sensor_readings.csv`. It contains two columns: `time` (in seconds) and `displacement` (in meters). The samples are not evenly spaced in time and contain measurement noise.

Your objectives are to determine the driving frequency using spectral analysis, fit a numerical ODE model to the data to extract the physical parameters, and visualize the result.

Perform the following steps:
1. **Data Preprocessing & Spectral Analysis:**
   - Read the data and interpolate it onto a uniform time grid from $t = 0$ to $t = 10$ seconds with a time step of $\Delta t = 0.01$ seconds using cubic spline interpolation.
   - Perform a Fast Fourier Transform (FFT) on the interpolated displacement data.
   - Identify the primary driving angular frequency, $\omega$ (in rad/s), which corresponds to the peak amplitude in the frequency spectrum (ignoring the DC/0 Hz component). Remember that $\omega = 2 \pi f$.

2. **Numerical ODE Modeling & Nonlinear Fitting:**
   - The system is governed by the second-order ordinary differential equation:
     $x''(t) + c \cdot x'(t) + k \cdot x(t) = F \cdot \sin(\omega t)$
   - Assume initial conditions $x(0) = 0.0$ and $x'(0) = 0.0$.
   - Write a simulation function that numerically integrates this ODE (e.g., using `scipy.integrate.solve_ivp`) for given parameters $c$ (damping), $k$ (stiffness), and $F$ (forcing amplitude).
   - Use a nonlinear least squares solver (e.g., `scipy.optimize.least_squares` or `curve_fit`) to find the optimal parameters `c`, `k`, and `F` that minimize the sum of squared differences between your ODE simulation and the *interpolated* data on the uniform time grid. 
   - Initial guesses for the optimizer: $c=1.0$, $k=20.0$, $F=1.0$.
   - Parameter bounds: $c \in [0.1, 5.0]$, $k \in [5.0, 50.0]$, $F \in [0.1, 10.0]$.

3. **Output & Visualization:**
   - Save the fitted parameters to a JSON file at `/home/user/model_params.json` with the exact keys: `"omega"`, `"c"`, `"k"`, `"F"`. Round the values to 3 decimal places.
   - Create a plot comparing the interpolated experimental data and the fitted ODE simulated trajectory. Save this plot to `/home/user/fit_comparison.png`.

Note: You will need to install any necessary Python libraries (e.g., scipy, numpy, pandas, matplotlib) using your terminal. Ensure your script handles the ODE integration accurately to allow the optimizer to converge.