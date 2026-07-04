You are a data engineer working on an ETL pipeline. Your task is to write a Python script `/home/user/etl_step.py` that processes a raw dataset, performs feature selection and engineering, and estimates a model parameter using bootstrap sampling. 

The dataset is located at `/home/user/sensor_data.csv` and contains continuous numerical columns: `F1`, `F2`, `F3`, `F4`, `F5`, and `Target`.

Your script must perform the following steps exactly:
1. Load the dataset using `pandas`.
2. Compute the Pearson correlation matrix to find the two features (out of `F1` to `F5`) that have the highest *absolute* correlation with the `Target` column.
3. Create a new engineered feature named `Interact` which is the element-wise product of these two selected features.
4. Set the NumPy random seed to `42` (`np.random.seed(42)`).
5. Perform bootstrap sampling to estimate the relationship between `Interact` and `Target`. Specifically, run exactly 1000 iterations where in each iteration you:
   - Sample the dataframe with replacement (sample size equal to the original dataframe length).
   - Fit a simple linear regression model using `sklearn.linear_model.LinearRegression(fit_intercept=False)` where `X` is the `Interact` column and `y` is the `Target` column.
   - Record the model's single coefficient.
6. Calculate the mean of these 1000 bootstrap coefficients.
7. Write the results to `/home/user/etl_output.txt` in the following format:
   - Line 1: The names of the two selected features, separated by a comma (alphabetical order, e.g., `F1,F4`).
   - Line 2: The mean of the bootstrap coefficients, rounded to exactly 4 decimal places.

Run your script to generate the output file.