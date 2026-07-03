You are a Machine Learning Engineer preparing synthetic training data for a spectroscopic denoising model. You need to write a Bash-based pipeline that performs a Monte Carlo simulation of noisy signals, validates them against analytical expectations to filter out extreme outliers, and packages the surviving data into an HDF5 file.

All your work should be done in `/home/user/ml_data_prep`.

**Step 1: Input Data**
You are provided with a file `/home/user/ml_data_prep/params.csv`. It contains 200 rows, each with two comma-separated values: `Amplitude,Seed`.
There is no header.

**Step 2: Monte Carlo Signal Generation & Validation**
Write a Bash script (e.g., using `awk`) that reads `params.csv` and processes each row as follows:
1. Initialize the random number generator with the given `Seed` (e.g., using `srand(Seed)` in `awk`).
2. Generate a 100-point signal $y_i$ for index $i = 0, 1, ..., 99$.
   The $x$-coordinate for each point is $x_i = i / 10$.
   The signal equation is: 
   $$y_i = A \cdot \exp\left(-0.5 \cdot (x_i - 5)^2\right) + N_i$$
   where $A$ is the `Amplitude` from the CSV, and $N_i$ is uniform random noise in the range $[-1.0, 1.0]$ generated using `(rand() - 0.5) * 2`. 
   *(Note: You must generate the 100 noise values in order from $i=0$ to $99$ after setting the seed once per row).*
3. **Analytical Validation:** Calculate the numerical integral of the generated signal using a simple left-Riemann sum: $\text{Area} = \sum_{i=0}^{99} y_i \cdot 0.1$.
   The analytical integral of the pure Gaussian on the infinite domain is $A \cdot \sqrt{2\pi} \approx A \cdot 2.506628$.
   If the absolute difference between the numerical $\text{Area}$ and the analytical integral is strictly less than `0.3`, the signal is considered valid.
4. For valid signals, output the 100 $y_i$ values as a comma-separated row to `/home/user/ml_data_prep/filtered.csv`.

**Step 3: Scientific Format Conversion**
Write a Python script to convert `/home/user/ml_data_prep/filtered.csv` into an HDF5 file `/home/user/ml_data_prep/spectra.h5`. 
The HDF5 file must contain a single dataset named `signals` of type `float64` containing the 2D array of the filtered signals (shape: `[N_valid, 100]`). You will likely need to use `h5py` and `numpy` (install them if necessary).

**Deliverables:**
Create a master executable script `/home/user/ml_data_prep/run.sh` that performs the entire pipeline from reading `params.csv` to producing `spectra.h5`. The automated test will execute this script and check the HDF5 output.