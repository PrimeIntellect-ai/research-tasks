You are a machine learning engineer preparing a training dataset. As part of your data cleaning pipeline, you need to find the mode of a continuous sensor variable to impute missing values.

A raw observational dataset is located at `/home/user/observations.csv`. It contains wide-format data with an `id` column and three sensor reading columns: `val_1`, `val_2`, and `val_3`.

Write a reproducible pipeline script at `/home/user/pipeline.py` that performs the following steps:
1. Reads `/home/user/observations.csv`.
2. Reshapes the observational data by extracting all values from the `val_1`, `val_2`, and `val_3` columns into a single flat 1D array.
3. Fits a probability density function to these values using `scipy.stats.gaussian_kde` with its default bandwidth estimator.
4. Uses numerical optimization (`scipy.optimize.minimize`) with an initial guess of `x0 = 0.0` to find the value `x` that maximizes the estimated probability density function.
5. Writes the optimal `x` value (the mode), rounded to exactly 3 decimal places, to the file `/home/user/result.txt`.

After writing the script, execute it to ensure the `/home/user/result.txt` file is generated correctly.