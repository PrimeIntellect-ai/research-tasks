You are a data engineer tasked with building an ETL pipeline that integrates linear algebra for feature extraction, trains an anomaly detection model, and leverages large-scale data storage formats. 

There is a raw dataset located at `/home/user/raw_transactions.csv`. This dataset contains 10,000 transaction records with the following columns: `transaction_id`, `amount`, `duration`, `location_score`, `network_latency`, and `device_trust`.

Your objective is to write and execute a Python script (`/home/user/pipeline.py`) that performs the following pipeline steps:

1. **Extract**: Load the CSV file into a pandas DataFrame.
2. **Transform (Linear Algebra & Feature Engineering)**:
    - Select the 5 numerical features: `amount`, `duration`, `location_score`, `network_latency`, and `device_trust`.
    - Standardize these 5 features so that each column has a mean of 0 and a standard deviation of 1.
    - Apply Principal Component Analysis (PCA) to reduce these 5 standardized features down to exactly **3 principal components**. Set `random_state=42` if your PCA implementation requires a seed.
3. **Transform (Model Training & Evaluation)**:
    - Train an `IsolationForest` model (from `sklearn.ensemble`) on the 3 principal components to detect anomalies. 
    - You MUST initialize the IsolationForest with `contamination=0.05` and `random_state=42`.
    - Predict the anomalies using the trained model (-1 indicates an anomaly, 1 indicates normal).
4. **Load (Large-scale Data Storage)**:
    - Filter the dataset to keep ONLY the anomalous records.
    - Append the 3 principal component columns to these anomalous records. Name them `pc1`, `pc2`, and `pc3`.
    - Save this filtered DataFrame (which should include the original columns plus the 3 PC columns) to a Parquet file at `/home/user/anomalies.parquet`. (You may need to install `pyarrow` or `fastparquet`).
    - Extract the PCA components matrix (the principal axes in feature space, which should be a 3x5 matrix). Save this matrix into an HDF5 file at `/home/user/model_data.h5` under the dataset name `pca_components`. (You may need to install `h5py`).

Before running your script, ensure you install any necessary Python packages (e.g., `pandas`, `scikit-learn`, `pyarrow`, `h5py`) into your environment.