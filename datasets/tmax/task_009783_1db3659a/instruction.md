You are a data analyst tasked with building a reproducible ETL and dimensionality reduction pipeline for manufacturing sensor data.

We have raw sensor readings from multiple machines stored as CSV files in the directory `/home/user/data/raw/`. 

Please write a Python script (or execute Python commands) to perform the following pipeline:

1. **Extract**: Load all CSV files from `/home/user/data/raw/`. Combine them into a single dataset.
2. **Transform (Filtering)**: 
   - Drop any rows that contain missing values (NaN) in any column.
   - Drop any rows where the value of `sensor_1` is strictly less than 0.
3. **Transform (Dimensionality Reduction)**:
   - Isolate the sensor columns (`sensor_1` through `sensor_20`).
   - Standardize these sensor features so that each column has a mean of 0 and a standard deviation of 1 (use `sklearn.preprocessing.StandardScaler`).
   - Apply Principal Component Analysis (PCA) to reduce the 20 sensor features down to exactly 3 principal components. 
   - Initialize your PCA with `random_state=42` to ensure strict reproducibility.
4. **Load (Output)**:
   - Create a final DataFrame that contains exactly the following columns in order: `timestamp`, `machine_id`, `PC1`, `PC2`, `PC3` (the three principal components).
   - Save this DataFrame to `/home/user/data/processed/pca_features.csv` without the index.
   - Extract the `explained_variance_ratio_` from the fitted PCA model. Save these three values as a comma-separated string (e.g., `0.1234,0.0567,0.0456`) into a text file at `/home/user/data/processed/explained_variance.txt`.

Make sure to create the `/home/user/data/processed/` directory if it does not exist.