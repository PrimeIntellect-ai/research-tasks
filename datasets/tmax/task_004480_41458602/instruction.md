You are a computational researcher analyzing the outputs of a recent molecular dynamics simulation. You need to process the raw trajectory data of a specific atom to establish a baseline for your automated regression tests.

The system state is saved in two files:
1. `/home/user/structure.pdb`: A PDB file containing the protein structure.
2. `/home/user/fluctuations.h5`: An HDF5 file containing the simulation time series. It has two datasets: `time` (in seconds) and `z_coord` (in Angstroms).

Your task is to write and execute a script (in any language of your choice) to perform the following analysis:
1. **Bioinformatics Parsing**: Parse `/home/user/structure.pdb` to identify the 3-letter Residue Name (e.g., ALA, GLY) for the atom with the serial number `145`.
2. **Data Extraction**: Read the `time` and `z_coord` arrays from `/home/user/fluctuations.h5`.
3. **Regression**: Fit a simple linear regression (line of best fit) to the `z_coord` vs. `time` data to determine the linear drift. Extract the slope of this line.
4. **Spectral Analysis**: Detrend the `z_coord` data by subtracting the fitted linear trend. Then, apply a Fourier Transform to the detrended data to find the dominant frequency (the frequency with the highest magnitude in the amplitude spectrum, ignoring the 0 Hz DC component).
5. **Regression Testing Baseline**: Save the results into a JSON file at `/home/user/baseline.json` exactly in this format:
```json
{
  "atom_145_residue": "RESIDUE_NAME",
  "drift_slope": 0.000,
  "dominant_frequency": 0.000
}
```
Replace `"RESIDUE_NAME"` with the extracted string. Replace the numeric values with your calculated results, rounded to exactly 3 decimal places.