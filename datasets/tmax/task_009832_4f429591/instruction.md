You are a Machine Learning Engineer preparing synthetic spectroscopic training data for a neural network. The physical model that generates the raw spectral peaks is written in C++ and uses a nonlinear solver to determine precise resonance frequencies. You need to compile this solver, run it, and write a Python script to process the resulting data, apply instrumental broadening, calculate distribution metrics, and log the convergence statistics.

Follow these exact steps:

1. **Compilation**: 
   A C++ source file is located at `/home/user/src/solver.cpp`. It simulates implicit anharmonic coupling by solving a nonlinear equation. Compile it using `g++` (require C++17) and output the executable to `/home/user/bin/solver`.

2. **Data Generation**:
   Run `/home/user/bin/solver`. It will automatically generate a CSV file at `/home/user/data/raw_peaks.csv` containing `intensity` and `frequency` columns. The solver will also print convergence information to standard output in the format: `Solver finished. Max convergence iterations: <X>`. Note this integer value `<X>`.

3. **Signal Processing & Metrics (Python)**:
   Write a Python script at `/home/user/process_spectra.py` that does the following:
   * Reads `/home/user/data/raw_peaks.csv`.
   * Generates a continuous "clean" spectrum $S(f)$ on a frequency grid from $f=0$ to $f=100$ consisting of exactly 1000 evenly spaced points (use `numpy.linspace(0, 100, 1000)`).
   * For each peak in the CSV, adds a Gaussian profile to the clean spectrum: $S(f) = \sum I_i \cdot \exp\left(-\frac{(f - f_i)^2}{2\sigma^2}\right)$, where $I_i$ is the intensity, $f_i$ is the frequency, and the instrumental broadening parameter $\sigma = 2.0$.
   * Sets the random seed using `numpy.random.seed(42)`.
   * Creates a "noisy" spectrum by adding uniform random noise sampled from $\mathcal{U}(0, 0.5)$ to the clean spectrum (one noise value per frequency bin).
   * Normalizes BOTH the clean and noisy spectra so that their sums equal 1.0 (treating them as probability mass functions).
   * Calculates the Wasserstein distance between the normalized clean spectrum and the normalized noisy spectrum. Use `scipy.stats.wasserstein_distance`. 
     *(Note: Pass the frequency grid as the `u_values` and `v_values`, and the normalized spectra as `u_weights` and `v_weights`)*.

4. **Output Logging**:
   The Python script (or a separate shell command) must create a JSON file at `/home/user/data/summary.json` containing exactly these two keys:
   * `"convergence_max_iterations"`: The integer parsed from the C++ solver's standard output.
   * `"wasserstein_distance"`: The calculated Wasserstein distance as a float, rounded to 6 decimal places.