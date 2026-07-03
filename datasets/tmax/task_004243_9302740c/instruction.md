You are a Data Scientist tasked with modernizing a legacy data pipeline. We have a proprietary, highly accurate but extremely slow legacy inference engine (provided as a stripped binary) that scores sensor data. 

Your goal is to build an end-to-end ETL pipeline, perform feature engineering, and train a fast proxy model to replace the legacy engine.

1. **Data Cleaning & ETL**:
   You are provided with a raw, noisy dataset at `/app/data/train_raw.csv` (features `f0` to `f19`).
   - Construct an ETL pipeline to clean this data. Drop any rows containing missing values (NaNs).
   - Remove outliers: drop any rows where any feature value has a z-score absolute value > 3.0.

2. **Correlation and Covariance Analysis**:
   - Analyze the cleaned dataset.
   - Drop redundant features: if any pair of features has an absolute Pearson correlation coefficient > 0.85, keep the one with the lower index (e.g., keep `f2` and drop `f5`).
   - Save the final list of selected feature names (one per line) to `/home/user/selected_features.txt`.

3. **Ground Truth Generation & Inference Benchmarking**:
   - The legacy oracle is located at `/app/bin/legacy_oracle`. It takes two arguments: an input CSV and an output CSV path.
   - Run the legacy oracle on your cleaned training data to generate the target scores. Note: The oracle is notoriously slow.
   - Log the inference time of the oracle per 100 rows.

4. **Proxy Model Training & Experiment Tracking**:
   - Train a fast machine learning model (using your choice of language/framework) to predict the oracle's target scores using ONLY your selected features.
   - Implement experiment tracking: save your model's training metrics (e.g., MSE, R2) to a JSON file at `/home/user/experiment_log.json`.

5. **Final Integration**:
   - Create an executable wrapper script at `/home/user/predict.sh` that takes two arguments: `[input_csv_path]` and `[output_csv_path]`.
   - When called, `/home/user/predict.sh` must apply the exact same ETL cleaning, feature selection, and model inference to the new data, saving the predictions to the specified output path (with a single column `target` and a header).

The performance of your proxy model will be evaluated against the legacy oracle on a hidden test set. Your wrapper must execute at least 50x faster than the legacy oracle, and its predictions must achieve a Mean Squared Error (MSE) < 0.05 compared to the oracle's outputs.