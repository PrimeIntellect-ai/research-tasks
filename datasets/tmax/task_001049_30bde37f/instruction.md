You are an automation specialist for a health-tech company. We have an automated pipeline that processes irregular biometric sensor data, but our previous system broke. You need to write a new ETL workflow using **Rust**.

Here is your setup:
1. **Raw Data**: You have a CSV file located at `/app/data/raw_vitals.csv` containing raw, irregularly sampled sensor readings. The columns are: `timestamp` (Unix epoch milliseconds), `patient_name`, `heart_rate` (float), and `temperature` (float). 
2. **Config Scan**: We received an image scan of the patient anonymization registry at `/app/config_scan.png`. 

Your goal is to complete the following multi-stage workflow:

**Stage 1: Extraction & OCR**
Use `tesseract` to extract text from `/app/config_scan.png`. The image contains mapping rules in the format `Patient Name : AnonymizedUUID`. Save this mapping to a usable text file.

**Stage 2: Rust ETL Implementation**
Create a new Rust project at `/home/user/etl_pipeline`. Write a Rust application that does the following:
* **Joins & Merges**: Read the raw CSV and the extracted OCR mappings. Replace the `patient_name` column with the corresponding `AnonymizedUUID`. If a patient name is not in the mapping, drop those rows.
* **Resampling & Gap-Filling**: For each `AnonymizedUUID`, resample the time-series data to exact **1000 millisecond (1 second)** intervals. Start at the exact minimum timestamp for that specific patient and end at their exact maximum timestamp. Fill in missing values for both `heart_rate` and `temperature` using **linear interpolation**.
* **Normalization**: After interpolation, apply Min-Max normalization to the `heart_rate` and `temperature` columns across the entire dataset so their values scale strictly from `0.0` to `1.0`. Use the absolute min and max of the interpolated dataset for the scaling.

**Stage 3: Output**
Write the final processed dataset to `/home/user/processed_data.csv` with the headers:
`timestamp,anonymized_id,normalized_hr,normalized_temp`
Sort the output first by `anonymized_id` (alphabetically), then by `timestamp` (ascending).

Print any standard logs to stdout, but the final file must strictly match the output format. Your solution will be tested against a hidden reference dataset. The Mean Squared Error (MSE) of your interpolated and normalized values compared to our reference must be strictly less than 0.001.