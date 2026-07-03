You are an automation specialist tasked with building a mathematical data processing pipeline for medical telemetry data. 

We receive raw, messy CSV exports containing patient vitals. Some text fields in this CSV contain embedded newlines which routinely break naive parsers. You must write a Python script `/home/user/pipeline.py` that processes this data, and then set up its execution schedule.

Here are the requirements for your Python script:
1. **Input Data**: Read `/home/user/raw_telemetry.csv`. Handle embedded newlines in the `Notes` column correctly (do not silently drop rows).
2. **Data Masking**: Anonymize the `PatientName` column by replacing the plain text name with the first 8 characters of its SHA256 hash (in lowercase hex). Drop the `Notes` column entirely.
3. **Resampling & Gap-filling**: 
   - The data contains a `Timestamp` column. Convert it to a datetime type.
   - For each `PatientID`, resample the `HeartRate` to a **daily** frequency (calendar day). 
   - When multiple readings exist for a day, take the mathematical mean.
   - If a day has no readings, use forward-fill (ffill) to fill the gap, but with a limit of 1 day (do not forward-fill across 2 consecutive missing days). Leave remaining missing days as NaN.
   - After gap-filling, compute a **3-day rolling mean** of the daily heart rate for each patient. Name this new column `RollingHR`. Use `min_periods=1`.
4. **Data Sampling & Stratification**: 
   - Isolate the data for the *latest available calendar day* present in the overall dataset.
   - We need a stratified sample for an audit. Group the latest day's records by the `Condition` column. 
   - From each `Condition` group, randomly sample exactly 50% of the patients (round down if an odd number, e.g., 50% of 3 is 1). Use `random_state=42` in your sampling function to ensure reproducible results.
5. **Output**: Save the final stratified sample to `/home/user/audit_sample.csv` (include columns: `PatientID`, `PatientName`, `Condition`, `HeartRate`, `RollingHR`). Sort the final CSV by `PatientID` in ascending order.

Finally, handle the **Pipeline Scheduling**:
Create a shell script `/home/user/run_pipeline.sh` that executes your Python script. Ensure it has execute permissions. Then, write a cron schedule expression into `/home/user/cron.txt` that would execute `/home/user/run_pipeline.sh` every day at exactly 03:15 AM. The file should contain just the single cron line.

Constraints:
- You may use `pandas` and built-in Python libraries. 
- Do not use root/sudo privileges.