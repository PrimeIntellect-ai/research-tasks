You are assisting a computational biophysicist studying the vibrational modes of a synthetic peptide. They have written a basic simulation engine to model the peptide's primary oscillator, but the numerical integrator diverges (blows up) because the step size (`dt`) is too large. 

Your task is to fix the integration parameters via convergence testing, perform a spectral analysis on the resulting trajectory to find the dominant vibrational frequency, and compile the results.

Here is the setup:
1. The simulation engine is located at `/home/user/sim_engine.py`. It contains a function `run_simulation(dt, duration=50.0)` which returns a 1D numpy array representing the position trajectory of the peptide over time.
2. The sequence of the peptide is stored in `/home/user/peptide.fasta`.

Perform the following steps:
1. **Convergence Testing:** Write a Python script to test the following time steps (`dt`): `0.1`, `0.05`, `0.02`, `0.01`, `0.005`. Find the **largest** `dt` from this list that results in a stable trajectory. A trajectory is considered stable if the maximum absolute value of the position is less than `10.0` and contains no `NaN` values.
2. **Spectral Analysis:** Using the stable trajectory generated with the optimal `dt` (and default duration of 50.0), use `numpy.fft` or `scipy.fft` to compute the Real Fast Fourier Transform (rFFT). Find the dominant frequency in Hertz (Hz). *Note: Ignore the DC component (0 Hz); find the peak frequency among all frequencies > 0.*
3. **Sequence Parsing:** Parse `/home/user/peptide.fasta` to extract the raw amino acid sequence (ignoring the header).
4. **Reporting:** Create a JSON file at `/home/user/results.json` containing exactly these keys:
   - `"optimal_dt"`: The largest stable time step you found (float).
   - `"dominant_frequency_hz"`: The dominant frequency in Hz, rounded to 1 decimal place (float).
   - `"sequence"`: The parsed amino acid sequence (string).

You may use any terminal commands, create Jupyter notebooks, or write standard Python scripts to accomplish this. Do not modify `sim_engine.py`.