You are acting as a Data Scientist on our operations team. We have a daily pipeline that dumps raw sensor readings, but the upstream systems are currently buggy, producing messy data. We need you to build a robust Python cleaning and modeling pipeline.

Your task involves writing a Python script `/home/user/pipeline.py` that processes the dataset located at `/home/user/raw_data.csv`. You must run your pipeline to generate specific output files. You may install any necessary Python packages (like pandas, numpy, scikit-learn) using pip.

Here are the requirements for your pipeline:

**Phase 1: Data Schema Enforcement & Cleaning**
Read `/home/user/raw_data.csv`. The expected schema is:
- `id`: integer, must be >= 0
- `sensor_A`: float
- `sensor_B`: float
- `sensor_C`: float
- `status`: integer (0 or 1)

Your code must filter out any rows that violate this schema. Specifically:
1. Drop rows with missing (NaN/null) values.
2. Drop rows where `id` < 0.
3. Drop rows where `sensor_A`, `sensor_B`, or `sensor_C` cannot be parsed as valid floats (some contain strings like "ERR" or "NaN_value").
4. Drop rows where `status` is not exactly 0 or 1.
Save the cleaned dataset to `/home/user/cleaned_data.csv`.

**Phase 2: Feature Engineering**
Using the cleaned dataset, create a new feature named `interaction_AB`. 
The formula is: `interaction_AB = sensor_A * sensor_B`.
Make sure this column is added to the cleaned dataframe before proceeding.

**Phase 3: Sampling & Bootstrap Testing**
We need to estimate the mean of the new `interaction_AB` feature robustly.
Implement a bootstrap sampling method directly in your script:
1. Use exactly `N=1000` bootstrap iterations.
2. In each iteration, sample with replacement from the cleaned `interaction_AB` array (sample size equals the number of cleaned rows). Use `numpy.random.seed(42)` BEFORE you start the bootstrap loop to ensure reproducibility. Inside the loop, do not reset the seed; just use `numpy.random.choice`. (To be precise: set the seed once, then run 1000 iterations).
3. Calculate the mean of `interaction_AB` for each bootstrap sample.
4. Calculate the overall mean of these 1000 sample means, and the 95% confidence interval using the percentile method (2.5th and 97.5th percentiles of the 1000 means).
Save these results to `/home/user/bootstrap_results.json` with the exact keys: `"mean"`, `"ci_lower"`, `"ci_upper"`.

**Phase 4: Classification Model**
Finally, train a Logistic Regression model to predict the `status` flag.
1. Features (X): `sensor_A`, `sensor_B`, `sensor_C`, `interaction_AB`.
2. Target (y): `status`.
3. Split the cleaned dataset into 80% training and 20% testing sets using `sklearn.model_selection.train_test_split` with `random_state=42` and `shuffle=True`.
4. Train a default `sklearn.linear_model.LogisticRegression` on the training set (use `random_state=42` where applicable).
5. Evaluate the accuracy of the model on the test set.
Save a JSON file to `/home/user/model_metrics.json` with the key `"test_accuracy"` containing the floating-point accuracy score.

Run your script, ensure all output files are generated, and confirm that the JSON outputs reflect the exact numerical values derived from your deterministic random seeds.