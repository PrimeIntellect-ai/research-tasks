You are a machine learning engineer preparing training data for a Physics-Informed Neural Network (PINN). You need to generate a dataset of a damped harmonic oscillator's trajectory. You have a fast C implementation of the ODE solver (`/home/user/ode/simulator.c`) and a slow but trusted Python baseline (`/home/user/ode/baseline.py`).

Your tasks are:
1. Compile the C code into an executable named `fast_sim` in the `/home/user/ode` directory. Use `gcc` with the `-O3` and `-lm` flags.
2. Perform a regression test by running both solvers with the following arguments (in this exact order): mass `m=1.0`, spring constant `k=2.0`, damping `c=0.5`, end time `t_end=10.0`, and time step `dt=0.01`. Both simulators take these 5 arguments from the command line and output CSV data (columns: `t,x,v`) to standard output.
3. Calculate the maximum absolute difference in the `x` (position) column between the two outputs for this test run. Write this maximum difference (as a floating point number) to `/home/user/ode/regression_diff.txt`.
4. Generate the final training dataset by running your compiled `fast_sim` with parameters `m=1.0, k=5.0, c=0.1, t_end=20.0, dt=0.01`. Save the standard output directly to `/home/user/ode/train_data.csv`.

Ensure all files are created exactly at the specified paths.