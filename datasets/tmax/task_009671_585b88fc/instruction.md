You are assisting a computational physics researcher who is struggling with a Monte Carlo simulation of a spectrometer.

The researcher has a Python script at `/home/user/sim/spectro_mc.py` that simulates photon detections. It uses Python's `multiprocessing` to speed up the work. However, the simulation produces slightly different total energy results across different runs despite using fixed random seeds. The researcher suspects this non-reproducibility is due to the floating-point reduction order (e.g., adding results as they complete out-of-order).

Your task is to:
1. Identify and fix the non-reproducibility bug in `/home/user/sim/spectro_mc.py`. You must ensure that the total energy sum is deterministic and immune to process scheduling variations. Use `math.fsum` on a deterministically ordered flattened list of all simulated energies to compute the final `total_simulated_energy`.
2. The researcher also has raw observational data at `/home/user/data/obs_raw.csv`. The file contains rows of `timestamp,detector_id,energy_kev`. Extract all the `energy_kev` values as a 1D array.
3. Write a script `/home/user/analyze.py` that:
   - Imports or runs the fixed `spectro_mc.py` to get the list of all simulated photon energies (not just the sum, you may need to modify the script to return or save the full deterministic list of energies).
   - Loads the observational `energy_kev` data.
   - Computes the 2-sample Kolmogorov-Smirnov statistic between the observational energies and the simulated energies using `scipy.stats.ks_2samp`.
   - Calculates the `total_simulated_energy` using `math.fsum`.
   - Writes a JSON file to `/home/user/results.json` with the following structure (round all floats to exactly 6 decimal places):
     ```json
     {
       "total_simulated_energy": 12345.678901,
       "ks_stat": 0.123456,
       "p_value": 0.001234
     }
     ```

You will need to install any missing Python packages (like `scipy`, `numpy`) in the user environment (`pip install --user`).

Ensure your fixed simulation runs deterministically before generating the final JSON. Do not change the random seeds or the distribution parameters in `spectro_mc.py`.