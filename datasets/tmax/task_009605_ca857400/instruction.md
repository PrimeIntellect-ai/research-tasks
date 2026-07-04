You are a performance engineer analyzing a physical simulation application. The application simulates a damped harmonic oscillator, but the current numerical integrator (explicit Euler) is suffering from numerical divergence due to an unstable step size. 

Your task is to fix the integrator, run the simulation, and perform spectral and statistical analysis on the resulting stable time-series.

All your work must be done in `/home/user`.

**Phase 1: Fix the ODE Solver**
1. We have provided a skeleton C file at `/home/user/oscillator.c`. It currently uses the explicit Euler method for the system:
   $dy/dt = v$
   $dv/dt = -100y - 2v$
   with initial conditions $y(0) = 1.0, v(0) = 0.0$.
2. Modify `/home/user/oscillator.c` to use the **4th Order Runge-Kutta (RK4)** method.
3. Simulate from $t = 0.00$ to $t = 10.00$ inclusive, using a fixed step size of $dt = 0.01$ (this means you will have 1001 data points).
4. Have the program output the results to `/home/user/timeseries.csv` with each line formatted strictly as `t,y` (e.g., `0.000000,1.000000`).

**Phase 2: Spectral Analysis & Bootstrap Statistics**
Write a new C program, `/home/user/analyze.c`, that reads `/home/user/timeseries.csv` and performs the following analyses:

1. **Spectral Analysis (DFT):**
   Compute the Discrete Fourier Transform (DFT) of the $y$ values to find the dominant frequency. 
   - Search for frequencies $f$ in the range `[0.10, 5.00]` Hz, in increments of `0.01` Hz.
   - For a given frequency $f$, the transform magnitude is $|X(f)| = \sqrt{R^2 + I^2}$, where:
     $R = \sum_{n=0}^{1000} y_n \cos(2 \pi f t_n)$
     $I = -\sum_{n=0}^{1000} y_n \sin(2 \pi f t_n)$
   - Identify $f_{dom}$, the frequency that maximizes $|X(f)|$.

2. **Statistical Analysis (Bootstrap Confidence Interval):**
   Calculate the 95% Bootstrap Confidence Interval for the mean of the 1001 $y$ values.
   - Seed the random number generator exactly once using `srand(42);` before starting the bootstrap loops.
   - Perform $N = 1000$ bootstrap iterations.
   - In each iteration, sample 1001 values from your $y$ array *with replacement*. To select an index, strictly use `rand() % 1001`.
   - Calculate the mean of these 1001 sampled values and store it.
   - Sort the 1000 bootstrap means in ascending order.
   - The 95% CI lower bound is the value at index 24 (the 25th value, 0-indexed).
   - The 95% CI upper bound is the value at index 974 (the 975th value, 0-indexed).

**Phase 3: Reporting**
Your `analyze.c` program should create a file `/home/user/report.txt` with exactly this format:
```
Dominant Frequency: <f_dom> Hz
Mean CI: [<lower_bound>, <upper_bound>]
```
Format the floats to 4 decimal places (e.g., `1.5800`).

Compile and run your code, ensuring the `report.txt` file is generated correctly.