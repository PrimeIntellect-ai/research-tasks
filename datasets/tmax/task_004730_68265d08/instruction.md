You are a Machine Learning Engineer tasked with preparing a reproducible data pipeline for high-dimensional server telemetry data. We need to compress the features using dimensionality reduction, evaluate the information loss (numerical accuracy of reconstruction), and train an anomaly detection model on the reduced dataset.

The raw data is located at `/home/user/telemetry.csv`.

Your task is to write a Python script (e.g., `pipeline.py`) that performs the following steps in order:

1. **Data Loading & Preprocessing:** 
   - Load `/home/user/telemetry.csv` using pandas.
   - Standardize all features using `sklearn.preprocessing.StandardScaler`.

2. **Dimensionality Reduction:**
   - Apply Principal Component Analysis (PCA) to reduce the data to exactly `5` components. 
   - Set `random_state=42` in the PCA initialization.

3. **Numerical Accuracy Testing:**
   - Inverse-transform the 5-component PCA data back to the original feature space.
   - Calculate the Mean Squared Error (MSE) between the *standardized original data* and the *PCA-reconstructed data*.

4. **Model Training & Evaluation:**
   - Train an `IsolationForest` on the 5-component PCA-transformed data to detect anomalies.
   - Set `random_state=42` for the IsolationForest.
   - Predict the anomalies (a prediction of `-1` indicates an anomaly). Count the total number of anomalies detected.

5. **Reporting:**
   - Export your results to a JSON file at `/home/user/metrics.json` with the following exact keys:
     - `"reconstruction_mse"`: The calculated MSE as a float, rounded to exactly 4 decimal places.
     - `"anomaly_count"`: The integer count of detected anomalies.

Ensure your pipeline is completely reproducible. You may install any necessary Python packages (like `scikit-learn`, `pandas`, `numpy`) if they are not already installed.