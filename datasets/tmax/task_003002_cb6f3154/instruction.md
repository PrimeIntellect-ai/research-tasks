I am preparing training data for a machine learning model, but my pipeline is giving non-reproducible results. 

The Bash script `/home/user/build_dataset.sh` processes a set of ODE simulation trajectories, extracts a characteristic value (simulating a dominant singular value from matrix decomposition), and aggregates them to compute a 1D probability distance metric (similar to Wasserstein distance). 

Because the script uses `xargs -P 4` to parallelize extraction, the values are appended to `/home/user/singular_values.txt` in a non-deterministic order. The final step uses an `awk` command that incorporates the row number (`NR`) to compute the distance metric. Since the lines are in a random order, this floating-point reduction produces a different result every time!

Please fix the `/home/user/build_dataset.sh` script. You must:
1. Ensure the parallel extraction still functions efficiently.
2. Make the final probability distance calculation strictly reproducible by sorting the contents of `/home/user/singular_values.txt` numerically in **ascending order** *before* the `awk` command processes it. 
3. Run your fixed script so that it produces the correct, reproducible value in `/home/user/training_label.txt`.

Do not change the mathematical formula in the `awk` command, just ensure it receives sorted input.