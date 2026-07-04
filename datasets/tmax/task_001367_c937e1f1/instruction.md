I am a researcher studying a highly damped nonlinear system modeled as a Van der Pol oscillator. I have experimental data for the system's position over time, but I need to determine the exact damping parameter, `mu` ($\mu$).

The system is defined by the following ODEs:
$dy_0 / dt = y_1$
$dy_1 / dt = \mu (1 - y_0^2) y_1 - y_0$

Initial conditions are $y_0(0) = 2.0$ and $y_1(0) = 0.0$.

I tried writing a script to optimize `mu` to fit the data, but my numerical integrator hangs or diverges because the system becomes highly stiff for large values of `mu`. 

Your task is to:
1. Read the target time `t` and position `y` (which corresponds to $y_0$) from the HDF5 file located at `/home/user/vdp_target.h5`.
2. Write a Python script `/home/user/solve.py` that defines an objective function to compute the Mean Squared Error (MSE) between the simulated $y_0$ values and the target `y` values at the exact same time points.
3. In your objective function, use `scipy.integrate.solve_ivp` to simulate the system. **Crucially, you must use a solver suited for stiff problems (like `Radau` or `BDF`)** so it doesn't diverge or hang.
4. Use `scipy.optimize.minimize` (the default Nelder-Mead or any derivative-free method is recommended to avoid finite-difference noise from the ODE solver) to find the optimal `mu`. Use an initial guess of `mu = 250.0`.
5. Once the optimization finishes, save the optimized value of `mu` to a text file `/home/user/optimized_mu.txt`, rounded to exactly 2 decimal places (e.g., `450.12`).

Ensure your script works efficiently and accurately, and execute it to produce the final text file. You may install `numpy`, `scipy`, and `h5py` via pip if they are not already installed.