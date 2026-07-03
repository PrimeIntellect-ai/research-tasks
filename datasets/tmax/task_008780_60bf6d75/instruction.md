You are a Machine Learning Engineer preparing physics-based synthetic training data for a surrogate model. You have a reference dataset containing real-world observations of a damped harmonic oscillator, but you need to find the correct damping coefficient ($c$) to generate matching simulation data.

You have been provided with a reference data file at `/home/user/reference.h5`. It contains a single HDF5 dataset named `y_ref`, representing the position $y(t)$ of the oscillator at 100 evenly spaced time steps from $t=0$ to $t=10$.

The system is governed by the second-order Ordinary Differential Equation (ODE):
$$ y'' + c y' + k y = 0 $$
where mass $m=1$, spring constant $k=10$, initial position $y(0) = 1.0$, and initial velocity $y'(0) = 0.0$.

Your task:
1. Write a Python script `/home/user/find_damping.py` that solves this ODE numerically for different candidate values of $c \in \{0.1, 0.5, 1.0, 1.5, 2.0\}$.
2. For each candidate $c$, calculate the Mean Squared Error (MSE) between your numerical solution $y(t)$ and the reference dataset `y_ref` loaded from `/home/user/reference.h5`.
3. Identify the value of $c$ that produces the lowest MSE.
4. Use a bash command to echo the best $c$ value into a log file at `/home/user/best_c.log` in the exact format: `BEST_C=X.X` (where X.X is the winning value).

Constraints:
- Use `scipy.integrate.odeint` or `solve_ivp` for the ODE solving.
- Use `h5py` to read the HDF5 file.
- The time vector must be exactly 100 evenly spaced points between 0 and 10, inclusive: `numpy.linspace(0, 10, 100)`.