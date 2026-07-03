As a performance and reliability engineer, you have been tasked with debugging a scientific data pipeline. 

We have a script at `/home/user/aggregate_power.py` that processes sensor network data from an HDF5 file (`/home/user/data.h5`). The script performs the following operations:
1. Reads a graph of sensor connections and raw time-series signals from the HDF5 file.
2. Uses a graph algorithm to find the largest connected component of sensors.
3. Computes the peak spectral power of each sensor in that component using a Fast Fourier Transform (FFT).
4. Sums the peak powers to produce a single global metric.

**The Problem:**
The script currently produces non-reproducible results. Because it uses unordered multiprocessing and processes nodes from an unordered `set`, the floating-point reduction order changes between runs. Since floating-point addition is not strictly associative, this leads to slightly different final metrics on every execution, failing our reproducibility tests.

**Your Task:**
1. Fix the script so that the computational pipeline is perfectly reproducible.
   - You must sort the node IDs of the largest connected component in ascending order before extracting their signals.
   - You must ensure the FFT peak powers are aggregated (summed) in that exact sorted order, removing any non-deterministic multiprocessing reduction (e.g., replace `imap_unordered` with a deterministic mapping or sequential execution).
   - Use standard Python floating-point addition (do not round intermediate steps).
2. Save your corrected script to `/home/user/fixed_aggregate.py`.
3. Run your fixed script and save its standard output (the final scalar float value) into a text file at `/home/user/stable_result.txt`.

Ensure your environment has the necessary scientific packages (e.g., `h5py`, `numpy`, `networkx`) installed if they aren't already.