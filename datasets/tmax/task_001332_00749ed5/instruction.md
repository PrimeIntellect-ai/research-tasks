You are a performance engineer tasked with profiling and fixing a custom molecular dynamics simulation package, `pydynsim`. 

We have provided the source code for the package in a vendored directory at `/app/vendored/pydynsim-1.2.0`. Currently, when researchers try to use it to simulate protein bond vibrations, the numerical integrator diverges after a few steps. Preliminary profiling indicates that this divergence is due to an incorrect step-size adaptation calculation in the integrator code (`pydynsim/integrator.py`). 

Your tasks are as follows:

1. **Fix the Package**: Inspect `/app/vendored/pydynsim-1.2.0/pydynsim/integrator.py`. The adaptive step size update is conceptually flawed (it increases the step size when the local truncation error is high, rather than decreasing it). Fix the mathematical typo in the adaptation logic. The correct scaling factor for the new step size should be `(tolerance / error)**0.5`. Install the fixed package into the system Python environment.

2. **Run and Analyze**: Write a Python script at `/home/user/analyze.py` that does the following:
   - Uses the fixed `pydynsim` package to parse the provided PDB file at `/app/data/protein.pdb` and runs a simulation for 5000 steps using the `pydynsim.simulate(filepath, steps=5000)` function.
   - The `simulate` function returns a numpy array of shape `(steps, num_atoms, 3)` containing the 3D coordinates over time.
   - Extract the timeseries of the Z-coordinate (index 2) for the atom with ID `5` (0-indexed atom index 4 in the array).
   - Perform a Fourier transform (FFT) on this Z-coordinate timeseries to compute the Power Spectral Density.
   - Determine the dominant vibrational frequency (the frequency with the highest spectral power). Assume the simulation time step `dt` (after adaptation settling) averages out to exactly `0.01` picoseconds for the purpose of the FFT frequency bin calculation.
   
3. **Report**: Save ONLY the dominant frequency (as a single floating-point number, in THz / inverse picoseconds) to `/home/user/frequency.txt`.

Ensure your fix prevents the simulation from returning `NaN`s, and that your spectral analysis correctly identifies the main vibrational mode of the specified atom.