You are a data scientist modeling the reaction kinetics of a newly sequenced enzyme. You have been provided with several files in `/home/user/`:

1. `simulate_experiment.c`: A C program that simulates the noisy experimental data of the reaction.
2. `enzyme.fasta`: A FASTA file containing the sequence of the enzyme.
3. `fit_kinetics.py`: A Python script intended to fit our kinetic model to the experimental data, but it is currently failing.

Your task is to complete the following pipeline:

**Phase 1: Data Generation**
1. Compile `simulate_experiment.c` into an executable named `simulate`. It requires the standard math library.
2. Run `./simulate` to generate `experimental_data.csv`.
3. Write a short Python snippet to convert `experimental_data.csv` into an HDF5 file named `/home/user/experimental_data.h5`. The HDF5 file should contain two datasets: `time` and `concentration`.

**Phase 2: Parameter Extraction**
Parse `/home/user/enzyme.fasta` using Python. The forward reaction rate constant, $k_1$, is derived from the enzyme's length:
$k_1 = \frac{\text{Number of amino acids in the sequence}}{100.0}$

**Phase 3: Model Fitting & Debugging**
The script `fit_kinetics.py` attempts to model the system:
$dA/dt = -k_1 A + k_2 B$
$dB/dt = k_1 A - k_2 B$
with $A(0) = 100, B(0) = 0$. 

It tries to fit the reverse rate constant, $k_2$, to the experimental data (which tracks $A$). However, the script uses a naïve forward Euler integrator with a very large step size that causes the numerical integration to diverge (producing infinities/NaNs), leading to a failed fit.
1. Modify `fit_kinetics.py` to read the `time` and `concentration` datasets from `experimental_data.h5`.
2. Insert your calculated $k_1$ into the script.
3. Fix the numerical divergence issue in `fit_kinetics.py`. You may replace the custom Euler integrator with `scipy.integrate.solve_ivp` (recommended to use a stable method like 'Radau' or 'BDF', or just 'RK45' with appropriate step sizes) or implement a stable integration scheme so that `scipy.optimize.curve_fit` can successfully find $k_2$.
4. Generate a plot named `/home/user/fit_plot.png` showing the experimental data as a scatter plot and the fitted curve as a solid line.

**Phase 4: Output**
Write the successfully fitted value of $k_2$ to `/home/user/result.txt` in the exact format:
`k2=X.XXX`
(Replace `X.XXX` with the value rounded to exactly three decimal places).