You are a bioinformatics analyst tasked with modeling the rapid selection dynamics of a novel viral variant. Your lab uses a Python script, `/home/user/simulate_selection.py`, to integrate an ordinary differential equation (ODE) that predicts the variant's allele frequency over time. 

Unfortunately, the script is currently failing. It uses a naive numerical integration scheme that diverges (producing `NaN` or `Inf` values) due to numerical instability and stiff model parameters.

Your task is to fix the script and generate the correct simulation output.

Here are your specific requirements:
1. Create a Python virtual environment at `/home/user/venv` and install the necessary scientific packages (`numpy`, `scipy`, `h5py`).
2. Modify `/home/user/simulate_selection.py` to fix the numerical instability. You should replace the custom explicit Euler integrator with `scipy.integrate.solve_ivp` using a solver suitable for stiff equations (e.g., `BDF`, `Radau`, or `LSODA`).
3. The script must read the initial frequency (`y0`), growth rate (`r`), and mutation penalty (`m`) from the HDF5 file `/home/user/params.h5` under the dataset names `y0`, `r`, and `m` respectively.
4. The simulation should run from `t = 0` to `t = 10` with continuous output evaluated at 1000 evenly spaced time points (using `np.linspace(0, 10, 1000)`).
5. The ODE is defined as: `dy/dt = r * y * (1 - y) - m * y`
6. Save the resulting simulated time points (the 1000 time values) and the corresponding allele frequencies (the 1000 `y` values) to a new HDF5 file at `/home/user/results.h5`. The file must contain two datasets: `time` (1D array) and `frequency` (1D array).

Complete these steps and ensure that `/home/user/results.h5` is successfully created with the stable simulation results.