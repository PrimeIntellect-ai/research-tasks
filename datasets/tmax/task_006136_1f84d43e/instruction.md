You are a data scientist tasked with cleaning a corrupted time-series dataset of medical sensor readings. 

The raw data is located at `/home/user/raw_sensor_data.csv`.

Here are the issues with the dataset and the steps you must take to process it:

1. **Broken CSV Format (Embedded Newlines)**: The dataset has 5 columns: `timestamp, patient_id, patient_name, heart_rate, notes`. Some of the `notes` fields are enclosed in double quotes but contain embedded newline characters (`\n`). This has broken standard line-by-line CSV parsers. You must safely parse the CSV, preserving the embedded newlines within the notes field, or standardizing them to spaces, before doing further processing.

2. **Data Masking & Anonymization**: 
    - The `patient_id` column contains sensitive identifiers in the format `SSN-XXXXXXXXX` (where X is a digit). You must use a regex pattern to mask all patient IDs to exactly `***-**-****`.
    - The `patient_name` column must be anonymized. Replace the plaintext name with the first 8 characters of its lowercase SHA-256 hex digest.

3. **Resampling and Gap-Filling**: 
    - The `timestamp` column contains ISO8601 formatted times (e.g., `2023-10-01T10:00:00`).
    - The sensor occasionally dropped connections, so there are gaps in the minute-by-minute data. 
    - For *each patient separately*, resample their time-series data to a strict **1-minute frequency**, starting from their earliest timestamp to their latest timestamp.
    - Use **forward-filling (ffill)** to fill missing `heart_rate` values and `notes` for the newly created timestamps.

4. **Mathematical Aggregation**:
    - After resampling and gap-filling, calculate the mean `heart_rate` for each anonymized patient.
    - Round the mean heart rate to exactly 2 decimal places.

**Outputs Required:**
1. Save the cleaned, anonymized, and resampled dataset to `/home/user/cleaned_data.csv`. It should have the same column order: `timestamp, patient_id, patient_name, heart_rate, notes`.
2. Save the aggregated mean heart rates to `/home/user/summary.json`. The JSON should be a dictionary where the keys are the anonymized patient names (the 8-char hex) and the values are the rounded mean heart rates (as floats). Example: `{"a1b2c3d4": 82.33, "f9e8d7c6": 79.0}`.