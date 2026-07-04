You are a Data Engineer building a machine-learning-driven ETL (Extract, Transform, Load) pipeline for an industrial IoT system. Your task is to write and execute a Python script (`/home/user/etl_pipeline.py`) that processes raw sensor data, extracts features, performs dimensionality reduction, and scores the records for anomalies.

The raw data is located at `/home/user/data/sensor_readings.csv`. It contains four columns: `timestamp`, `sensor_A`, `sensor_B`, and `sensor_C`.

Your pipeline must perform the following steps exactly as described to ensure reproducibility:

1. **Data Ingestion & Preparation**: Read the CSV file. Ensure the data is sorted chronologically by `timestamp`.
2. **Feature Engineering**: For each of the three sensor columns (`sensor_A`, `sensor_B`, `sensor_C`), calculate a rolling mean over a window of 3 time steps. Name these new columns `sensor_A_roll`, `sensor_B_roll`, and `sensor_C_roll`. Drop any rows that contain NaN values as a result of the rolling window.
3. **Correlation Analysis & Feature Selection**: Compute the Pearson correlation matrix for the 6 feature columns (excluding `timestamp`). To remove redundant features, check the absolute correlation between all pairs of features. If any pair has an absolute correlation >= 0.90, drop the feature whose column name is alphabetically later (e.g., if `sensor_A` and `sensor_B` have a correlation of 0.92, drop `sensor_B`). *Hint: Be careful to process pairs such that if a feature is dropped, it is no longer considered in subsequent pair comparisons.*
4. **Dimensionality Reduction**: Apply Principal Component Analysis (PCA) using `sklearn.decomposition.PCA` to reduce the remaining feature columns down to exactly 2 components. Set `random_state=42` when initializing PCA.
5. **Model Training & Inference**: Train an anomaly detection model on the 2 PCA components. Use `sklearn.ensemble.IsolationForest` with `random_state=42` and `contamination=0.1`. Fit the model on the PCA components, then generate the anomaly scores (using `decision_function`) and the binary anomaly labels (using `predict`).
6. **Data Loading (Output)**: Save the final processed records to `/home/user/output/final_pipeline_output.csv` without the index. The output CSV must contain exactly the following columns in this order:
   - `timestamp` (the original timestamp)
   - `pca_0` (the first PCA component)
   - `pca_1` (the second PCA component)
   - `anomaly_score` (the float score from IsolationForest)
   - `is_anomaly` (the integer prediction from IsolationForest: 1 for normal, -1 for anomaly)

Install any required dependencies (e.g., `pandas`, `scikit-learn`) using `pip`. Create the necessary output directories if they do not exist.