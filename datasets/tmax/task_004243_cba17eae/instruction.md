You are helping a computational physics researcher debug and analyze a simulation of a 1D wave system. 

The simulation code is located at `/home/user/sim/wave_sim.py`. The script uses domain decomposition to split the spatial mesh into multiple subdomains. At each time step, it computes a global system metric (referred to as "energy") by reducing (summing) the values from all subdomains. 

However, the researcher has noticed a problem: the simulation results are not perfectly reproducible. Running the script multiple times yields slightly different energy time-series. The researcher suspects this is due to floating-point addition order changing because the subdomain results are being aggregated in a non-deterministic order (simulating unpredictable thread completion times).

Your tasks are as follows:

1. **Environment Setup**:
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `numpy`, `scipy`, and `matplotlib` inside this virtual environment.
   - You must use this virtual environment for all subsequent Python execution.

2. **Fix the Reproducibility Bug**:
   - Inspect `/home/user/sim/wave_sim.py`.
   - Modify the global reduction step in the code so that the subdomains are ALWAYS summed in strictly ascending order based on their `id` attribute.
   - Run the simulation to generate the deterministic `/home/user/sim/energy.npy` file.

3. **Spectral Analysis**:
   - Write a new Python script at `/home/user/sim/analyze.py`.
   - This script must load `energy.npy` and perform a Fourier transform (FFT) on the time-series data to determine the dominant oscillation frequency. The simulation time step (`dt`) is `0.01` seconds.
   - Ignore the DC component (0 Hz) when finding the peak.
   - The script must write the single dominant frequency (in Hz) as a standard float to a text file at `/home/user/sim/peak.txt`.
   - The script must also generate a plot of the frequency spectrum (Amplitude vs Frequency) and save it to `/home/user/sim/spectrum.png`.

Please complete these steps using the terminal. Let me know when the fix is applied, the simulation is run, and the analysis is complete.