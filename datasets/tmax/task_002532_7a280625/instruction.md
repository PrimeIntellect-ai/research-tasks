You are a performance engineer tasked with optimizing a scientific data processing pipeline. 

We have a system of ordinary differential equations (ODEs):
dx/dt = -alpha * x + y^2
dy/dt = -x - alpha * y

We need to process a batch of initial conditions and parameters, simulate the system, and find the exact time `t` (where `t > 0`) at which `x(t) = y(t)` for the first time.

Currently, our pipeline is too slow and crashes. Your task is to write a highly efficient Python script at `/home/user/fast_analysis.py` that performs this analysis.

Requirements:
1. **Input:** Read the HDF5 file `/home/user/data/initial_conditions.h5`. It contains three 1D datasets: `x0`, `y0`, and `alpha` (all of the same length).
2. **ODE Solving & Root Finding:** For each triplet `(x0, y0, alpha)`, solve the ODE system starting from `t=0` with `x(0)=x0` and `y(0)=y0`. Find the first time `t > 0` where `x(t) - y(t) = 0`. You can assume the first root always occurs in the interval `0 < t <= 10.0`. 
3. **Output:** Create a NetCDF4 file at `/home/user/results/output.nc`. It must have:
   - A single dimension `index` corresponding to the number of initial conditions.
   - Four float64 variables: `x0`, `y0`, `alpha`, and `t_root`, indexed by the `index` dimension.
   - Populate these variables with the input values and the computed roots.
4. **Constraints:** Your script must execute and produce the correct output file. Use `scipy.integrate.solve_ivp` with `dense_output=True` and a root-finding method from `scipy.optimize` for an accurate and efficient solution.

Make sure to create the `/home/user/results/` directory if it does not exist. Run your script to generate the output file.