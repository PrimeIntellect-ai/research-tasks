You are a data scientist cleaning an experimental dataset collected from various laboratories. 

You have been given a CSV file at `/home/user/raw_data.csv` with the following columns:
`TrialID,LabName,Measurement`

The data is messy and requires processing. Write a Python script to process the data and generate a summary report.

Here are your data processing requirements:
1. **Normalization:** The `LabName` column contains inconsistent whitespace and casing (e.g., " Alpha ", "BETA", "alpha"). Normalize all lab names by stripping leading/trailing whitespace and converting them to completely lowercase.
2. **Deduplication:** After normalizing the lab names, there are completely identical duplicate rows (same TrialID, LabName, and Measurement). Remove these exact duplicates so only unique rows remain.
3. **Imputation:** The `Measurement` column has missing values (represented as empty strings `""` or the string `"NaN"`). Replace these missing values with the arithmetic mean of the valid measurements for that *specific* normalized lab. Round the imputed mean to 2 decimal places. 
4. **Sorting & Grouping:** Group the cleaned and imputed dataset by the normalized `LabName`.
5. **Template Generation:** For each lab (sorted alphabetically by the normalized lab name), generate a single line in an output text file at `/home/user/report.txt` using exactly this template:
`Lab: {lab_name} | Trials: {trial_count} | Avg: {lab_average}`

Where:
- `{lab_name}` is the normalized lab name.
- `{trial_count}` is the total number of unique trials for that lab after deduplication (including the imputed ones).
- `{lab_average}` is the average measurement of all trials for that lab (valid + imputed), formatted to 2 decimal places.

Run your script and ensure `/home/user/report.txt` is generated exactly as specified.