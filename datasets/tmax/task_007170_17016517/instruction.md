You are tasked with processing a dataset of sensor readings, building a dimensionality reduction pipeline, training a simple classifier, and benchmarking its inference time. 

You will find the dataset at `/home/user/sensor_data.csv`. The dataset contains 10 continuous sensor features (`sensor_1` to `sensor_10`), a categorical identifier (`machine_id`), and a binary target (`is_faulty`).

There is a subtle data quality issue: a missing value in the `machine_id` column has caused the data loading process in many tools (like pandas) to silently cast the entire `machine_id` column to floats. 

Perform the following steps:
1. **Data Cleaning & Feature Engineering**: Load the dataset. Fill any missing values in the `machine_id` column with the value `999`. Ensure that the `machine_id` column is properly cast to an integer type (it should not have decimal points when saved).
2. **Dimensionality Reduction**: Exclude `machine_id` and `is_faulty` from the features. Apply standard scaling (zero mean, unit variance) to the 10 sensor features. Then, use Principal Component Analysis (PCA) to reduce these scaled features down to exactly 3 principal components (name them `pc1`, `pc2`, `pc3`).
3. **Modeling**: Train a standard Logistic Regression model (with default hyperparameters) using only the 3 principal components to predict `is_faulty`.
4. **Output Validation**: Generate predictions for the entire training dataset. Save a new CSV file to `/home/user/predictions.csv` containing exactly the following columns in this order: `machine_id`, `pc1`, `pc2`, `pc3`, `prediction`. 
   *CRITICAL: The `machine_id` column in this output file must be formatted as integers (e.g., `5`, not `5.0`).*
5. **Inference Benchmarking**: Write a benchmark loop that takes a single new random observation (10 random float values drawn from a standard uniform distribution `[0, 1)`), applies the fitted scaler, applies the fitted PCA model, and generates a prediction using the fitted Logistic Regression model. Run this single-observation inference process 1,000 times sequentially. Calculate the *average* inference time per observation in milliseconds. Save this single numeric value (e.g., `1.45`) to a text file at `/home/user/benchmark.txt`.

You may use any programming language you prefer (Python is recommended). You will need to install any necessary packages (e.g., `pandas`, `scikit-learn`) yourself.