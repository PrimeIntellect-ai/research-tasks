You are an AI assistant helping a medical researcher process and score patient data. The researcher has provided you with raw data files and a simple model schema, but needs you to assemble the pipeline.

Your tasks are:
1. Extract the dataset `/home/user/data/demographics.tar.gz` which contains `demographics.csv`.
2. Join the extracted `demographics.csv` with `/home/user/data/biomarkers.csv` using the `patient_id` column.
3. Perform data cleaning:
   - Impute any missing `age` values with `50`.
   - Impute any missing `bmi` values with `25.0`.
   - Handle outliers in the `heart_rate` column: any value strictly greater than `150` must be clipped (set) to `150`.
4. Reconstruct and apply the risk scoring model. A JSON file at `/home/user/model/weights.json` contains the linear weights for the features (`age`, `bmi`, `heart_rate`). The model's risk score is calculated as the sum of the products of each feature and its corresponding weight.
5. Calculate the risk score for each patient.
6. Create an output CSV file at `/home/user/risk_scores.csv` with the headers `patient_id,risk_score`.
   - Format the `risk_score` to exactly 2 decimal places.
   - Sort the output by `patient_id` in ascending numerical order.

Ensure your final output file strictly matches the specified path, headers, and formatting. You may use standard Unix tools, Python, or bash commands to accomplish this task.