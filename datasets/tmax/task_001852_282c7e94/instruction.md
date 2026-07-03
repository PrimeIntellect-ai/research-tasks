You are a Machine Learning Engineer preparing a synthetic dataset of physical signals to train a neural PDE solver.

Your task is to generate a dataset of simple harmonic oscillator signals, assess the numerical stability/error of a basic solver, and extract spectral features.

Create a Bash script at `/home/user/build_dataset.sh` that orchestrates the data generation. It should execute a Python script (which you must also write) at `/home/user/generate_features.py`.

**Specifications for `/home/user/generate_features.py`**:
1. Accepts one integer CLI argument: `f` (the frequency in Hz).
2. Simulates the ODE $y'' + (2\pi f)^2 y = 0$ using the **Forward Euler** method. 
3. Initial conditions: $y(0) = 1.0$, $y'(0) = 0.0$.
4. Use a time step $dt = 0.01$ and compute exactly $100$ steps. You should produce $100$ points for $y(t)$ corresponding to $t = 0.00, 0.01, ..., 0.99$.
5. Evaluate the numerical stability and accuracy by calculating the **maximum absolute error** between your numerical $y(t)$ and the analytical solution $y_{exact}(t) = \cos(2\pi f t)$ over these 100 points.
6. Extract the dominant frequency by calculating the real Fast Fourier Transform (`numpy.fft.rfft`) of the numerical $y$ values. Use `numpy.fft.rfftfreq` with `d=0.01` to find the frequency bins. The peak frequency is the one corresponding to the maximum absolute magnitude in the FFT.
7. Print a single comma-separated line to stdout: `max_error,peak_freq`. Format `max_error` to exactly 4 decimal places and `peak_freq` to exactly 1 decimal place.

**Specifications for `/home/user/build_dataset.sh`**:
1. Must be executable.
2. Loops through frequencies $f \in \{1, 2, 3, 4, 5\}$.
3. Calls `generate_features.py` for each frequency.
4. Writes the results to `/home/user/dataset.csv`.
5. The CSV must have the header `f,max_error,peak_freq`.
6. Each subsequent line should contain the frequency and the output of the Python script.

Run your bash script to generate `/home/user/dataset.csv` before finishing.