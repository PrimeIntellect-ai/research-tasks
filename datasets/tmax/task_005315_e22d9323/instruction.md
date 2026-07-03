You are an ML engineer preparing training data from numerical simulations. The physics simulator uses 32-bit floats, and due to parallel reduction order differences across two different hardware nodes, the results are not perfectly reproducible.

You have been given two HDF5 files representing the output of the same simulation run on two different nodes:
- `/home/user/sim_v1.h5`
- `/home/user/sim_v2.h5`

Each file contains a single dataset named `features` of shape `(1000, 50)`. 

To ensure these numerical instabilities are within acceptable bounds for machine learning, you must write a Python script `/home/user/analyze_stability.py` that computes a bootstrap confidence interval of the differences between the datasets. 

Your script should perform the following steps:
1. Load the `features` dataset from both HDF5 files.
2. Calculate the absolute difference between the two datasets element-wise.
3. Compute the mean of these absolute differences for each row (resulting in an array of 1000 values).
4. Calculate a 95% bootstrap confidence interval of the mean of these 1000 values using exactly the following method to ensure reproducibility:
   - Use `numpy`.
   - Set the random seed to `42` (`np.random.seed(42)`).
   - Generate `1000` bootstrap resamples. Each resample must be generated using `np.random.choice(row_diffs, size=len(row_diffs), replace=True)`.
   - Calculate the mean of each resample.
   - Use `np.percentile` with `2.5` and `97.5` to find the lower and upper bounds of the confidence interval from the resample means.
5. Write the resulting lower and upper bounds to a text file `/home/user/stability_report.txt` in the following exact format:

```
Lower CI: <value rounded to 6 decimal places>
Upper CI: <value rounded to 6 decimal places>
```

Run your script to generate the `/home/user/stability_report.txt` file.