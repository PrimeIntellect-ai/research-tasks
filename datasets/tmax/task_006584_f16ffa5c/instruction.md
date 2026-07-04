You are a performance engineer profiling a computational biology application. A researcher has written a Python script located at `/home/user/analyze_signal.py` that processes synthetic spectroscopy data. The script performs kernel density estimation to find spectral peaks and then uses a simple optimization step to find the maximum intensity. 

Currently, the script is extremely slow because the density estimation function (`slow_density_estimation`) is implemented using naive, nested Python loops. 

Your task is to:
1. Profile the script to confirm the bottleneck.
2. Refactor the `slow_density_estimation` function in `/home/user/analyze_signal.py` to use fully vectorized NumPy operations instead of Python `for` loops. The mathematical output must remain exactly the same (to within standard floating-point precision).
3. Ensure the script executes successfully and runs significantly faster (it should easily complete in less than 1 second).
4. Run the optimized script so that it generates the output file at `/home/user/result.txt`.

The output file `/home/user/result.txt` will contain the x-coordinate of the maximum density peak, formatted to 4 decimal places. Do not change the random seed or the grid parameters in the `main` function.