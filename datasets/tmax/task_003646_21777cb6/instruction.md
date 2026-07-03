You are an AI assistant helping a machine learning engineer prepare synthetic training data. We need to generate a dataset of correlated multivariate normal random variables that adhere to a specific target covariance matrix. We also need to set up a regression test to ensure our generation logic remains correct over time.

Your task is to:
1. Create a Python script `/home/user/generate_data.py` that reads a 3x3 covariance matrix from `/home/user/target_cov.json` (which is already provided to you).
2. In this script, use Monte Carlo simulation and Cholesky decomposition to generate 100,000 samples of 3D zero-mean normal random variables with the specified covariance. 
   - You must set the numpy random seed to `42` before generating the standard normal base samples.
   - Save the generated data to `/home/user/synthetic_data.csv` with a header `f1,f2,f3` and 6 decimal places of precision.
3. Create a test script `/home/user/test_generator.py` using `pytest`. This test should:
   - Run the generation logic or load the generated `/home/user/synthetic_data.csv`.
   - Calculate the empirical covariance matrix of the generated data.
   - Load the target covariance from `/home/user/target_cov.json`.
   - Assert that the absolute difference between every element of the empirical covariance matrix and the target covariance matrix is strictly less than `0.05` (use `np.allclose` or manual checks).
4. Run your data generation script.
5. Run your test using `pytest /home/user/test_generator.py > /home/user/test_results.log`.

Ensure all files are located in `/home/user/` and named exactly as specified.