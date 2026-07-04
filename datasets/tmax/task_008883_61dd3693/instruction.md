You are a bioinformatics analyst processing nanopore sequence data. We use a physical ODE model to filter observational signal data before visualization. The model is a simple low-pass filter described by the differential equation:

dy/dt = (x(t) - y(t)) / tau

Where `x(t)` is the raw nanopore signal, `y(t)` is the filtered signal, and `tau` is the time constant of the pore (tau = 0.01 seconds). 

We have a C program at `/home/user/nanopore_filter.c` that reads the sequence data from `/home/user/raw_signal.csv` and integrates this ODE using the explicit Euler method. However, the observational data is sampled at `dt = 0.05` seconds. Because `dt > 2 * tau`, the numerical integrator diverges and outputs `NaN` / `Inf` values due to poor step-size adaptation.

Your task:
1. Modify the C code in `/home/user/nanopore_filter.c` to use a sub-stepping approach. Instead of a single step of `dt = 0.05`, perform `N = 10` sub-steps of size `h = dt / 10 = 0.005` between each observational data point. 
2. During the sub-steps between `t_{i-1}` and `t_i`, assume the input signal `x(t)` is constant and equal to the newly read value `x_i`.
3. Compile the modified C program.
4. Run the program to process `/home/user/raw_signal.csv`.
5. Redirect the standard output of the fixed program to a new file at `/home/user/filtered_signal.csv`.

The output file `/home/user/filtered_signal.csv` must contain two comma-separated columns: `Time` and `FilteredSignal` (matching the input rows exactly, printing only at the observational time points, not the sub-steps).