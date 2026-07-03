You are acting as a scientific computing assistant for a researcher running simulations. 

The researcher has an old simulation script `/home/user/legacy_sim.py` and a newly optimized version `/home/user/fast_sim.py`. Both scripts take a single integer random seed as a command-line argument and output a 2D numpy array (shape: 1000 samples by 50 features) saved as `legacy_out.npy` and `fast_out.npy`, respectively. The new version is supposed to produce statistically identical results, but there might be slight numerical differences due to vectorization and precision changes.

Your task is to write and execute a regression testing script at `/home/user/regression_test.py` that does the following:
1. Executes `legacy_sim.py` and `fast_sim.py`, passing the random seed `12345` to both.
2. Loads the resulting `legacy_out.npy` and `fast_out.npy` files.
3. Iterates over each of the 50 features (columns) and calculates the 1st Wasserstein distance between the legacy and fast distributions for that feature. Use `scipy.stats.wasserstein_distance` for this metric.
4. Finds the maximum Wasserstein distance across all 50 features.
5. Writes this maximum distance to a file named `/home/user/max_wasserstein.txt`, formatted to exactly 6 decimal places (e.g., `0.001234`).
6. Exits with code 0 if the maximum distance is less than `0.01`, otherwise exits with code 1.

Run your script to generate the text file and verify the exit code. Ensure that `scipy` is installed.