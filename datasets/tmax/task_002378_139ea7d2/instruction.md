You are an AI assistant helping a physical chemistry researcher simulate a time-resolved spectroscopy experiment. We have a theoretical kinetic model and a C code that generates pure-component spectra. You need to compile the C code, solve the kinetic equations, combine the results, and analyze the simulated data using Singular Value Decomposition (SVD).

Please perform the following steps:

1. **Compile the Spectral Library**:
   In `/home/user/sim_project`, there is a file named `spectrum_gen.c`. Compile it into a Linux shared library named `libspectrum.so` in the same directory. Note that it requires the math library (`-lm`).

2. **Simulate the Kinetics (ODE Solving)**:
   Write a Python script `/home/user/sim_project/simulate.py`.
   Use `scipy.integrate.solve_ivp` to solve the following reaction system ($A \rightarrow B \rightarrow C$):
   * $dA/dt = -0.5 A$
   * $dB/dt = 0.5 A - 0.2 B$
   * $dC/dt = 0.2 B$
   * Initial conditions at $t=0$: $A=1.0, B=0.0, C=0.0$.
   * Evaluate the solution over the time interval $t \in [0, 10]$ at exactly 100 evenly spaced time points (e.g., using `numpy.linspace(0, 10, 100)`).
   * This will yield a Concentration matrix $C_{mat}$ of shape `(100, 3)` where the columns represent A, B, and C respectively.

3. **Generate Pure Spectra**:
   In your Python script, use `ctypes` to load the `libspectrum.so` library.
   The library exposes a single function with the following signature:
   `void get_spectrum(int comp_id, double* out_array, int length);`
   * Call this function for `comp_id` 0, 1, and 2 (corresponding to A, B, and C).
   * Use a `length` of 200 for each.
   * Store the results to form a Spectral matrix $S_{mat}$ of shape `(3, 200)`.

4. **Construct and Decompose the Data Matrix**:
   * Compute the simulated experimental data matrix $M = C_{mat} \times S_{mat}$. The resulting matrix $M$ should have the shape `(100, 200)`.
   * Perform a Singular Value Decomposition (SVD) on $M$ using `scipy.linalg.svd`.
   * Extract the first (largest) 3 singular values.
   
5. **Output**:
   * Save these 3 singular values to `/home/user/sim_project/singular_values.txt`.
   * The file should contain a single line with the 3 values separated by commas, formatted to exactly 4 decimal places (e.g., `12.3456,7.8901,2.3456`).

Execute your Python script to generate the final output file.