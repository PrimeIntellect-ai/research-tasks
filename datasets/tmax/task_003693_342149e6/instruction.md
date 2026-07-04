I am a researcher organizing some sensor datasets, but my analysis script is currently broken. I have a script located at `/home/user/analyze.py` that reads a dataset from `/home/user/sensordata.csv`. The script is supposed to calculate the covariance and Pearson correlation matrices for the sensor readings and plot a heatmap of the correlation matrix.

However, I am running into several issues:
1. The script produces a blank or broken plot when saving to `/home/user/heatmap.png` because the plotting library backend is misconfigured for a headless Linux environment.
2. The script uses a custom, naive numerical implementation for calculating covariance and correlation. Due to the very large baseline offsets in my sensor data, this naive implementation suffers from catastrophic cancellation, resulting in completely inaccurate correlation values (sometimes outside the [-1, 1] range) and incorrect covariances.

Your task is to:
1. Fix the matplotlib backend misconfiguration in `/home/user/analyze.py` so that it successfully saves a proper, non-blank plot to `/home/user/heatmap.png`.
2. Replace the custom `naive_cov` and `naive_corr` logic with robust, numerically stable implementations (you may use standard functions from `pandas` or `numpy`). Ensure that the sample covariance (with Bessel's correction, degrees of freedom = N-1) is used.
3. The script should output the corrected correlation matrix to `/home/user/correlation.csv` and the covariance matrix to `/home/user/covariance.csv`. The output CSV files must retain the column and row headers corresponding to the sensor names (columns from the input CSV), and all numerical values must be rounded to exactly 4 decimal places.

Please run the fixed script and verify that the output CSV files contain correct, stable values and that the heatmap is generated successfully.