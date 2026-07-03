You are a data scientist tasked with cleaning and normalizing a batch of messy physiological datasets from several hospitals. The raw data contains sensitive Protected Health Information (PHI) and is currently in an unwieldy "wide" format with inconsistent timezones.

Your goal is to write and execute a Python ETL pipeline that processes these files in parallel, anonymizes the data, reshapes it, normalizes timestamps, and logs the process.

**Input Data:**
There are 4 CSV files located in `/home/user/raw_data/` (e.g., `hospital_1.csv`, `hospital_2.csv`, etc.).
Each CSV has the following columns:
`patient_name`, `ssn`, `record_date` (format: YYYY-MM-DD), `tz` (e.g., 'America/New_York', 'Europe/London'), `HR_00:00`, `HR_06:00`, `HR_12:00`, `HR_18:00`.
The `HR_*` columns contain heart rate measurements taken at those specific local times on the `record_date`.

**Processing Requirements:**
Create a Python script at `/home/user/pipeline.py` that accomplishes the following:
1. **Parallel Processing:** Use Python's `multiprocessing` or `concurrent.futures` to process the 4 CSV files in parallel.
2. **Data Anonymization (Masking):** 
   - Drop the `patient_name` column entirely.
   - Replace the `ssn` column with a new column `patient_id` which is the SHA-256 hexadecimal digest of the `ssn` string.
3. **Reshaping (Wide to Long):**
   - Melt the `HR_*` columns so that each row represents a single measurement. The resulting columns should be `patient_id`, `record_date`, `tz`, `time_of_day` (e.g., '00:00', '06:00'), and `heart_rate`.
   - Drop rows where `heart_rate` is missing (NaN or empty).
4. **Timestamp Alignment:**
   - Combine `record_date`, `time_of_day`, and `tz` to create a single timezone-aware UTC datetime. 
   - Add this as a new column named `utc_timestamp` formatted as an ISO8601 string ending in 'Z' (e.g., `2023-10-15T04:00:00Z`).
   - Drop the `record_date`, `tz`, and `time_of_day` columns.
5. **Output:** 
   - Save the cleaned, long-format data for each input file as a Parquet file in `/home/user/clean_data/`. 
   - The output filenames should match the input filenames but with a `.parquet` extension (e.g., `hospital_1.parquet`).
6. **Logging:**
   - Configure Python's standard `logging` module to write to `/home/user/pipeline.log`.
   - For each file processed successfully, log an INFO message exactly in this format: `Successfully processed <filename> - <N> records generated` (where `<N>` is the number of rows in the final long-format DataFrame for that file).

**Environment Setup:**
You will need to install any required libraries (e.g., `pandas`, `pyarrow`, `pytz`) using pip.
Ensure the output directory `/home/user/clean_data/` exists before saving files.

Run your script to complete the task.