You are an automation specialist for a health-tech research lab. You have received a batch of raw patient data files in CSV format that must be processed before they can be shared with researchers. The files are located in `/home/user/raw_data/`.

You need to write a master Bash script at `/home/user/workflow.sh` that processes all `.csv` files in the input directory and writes the cleaned, anonymized files to `/home/user/processed_data/` (creating the directory if it doesn't exist). The files must be processed in **parallel** using `xargs` or `GNU parallel` to ensure the workflow scales.

The raw CSV files have the following header:
`PatientID,Name,SSN,Age,BloodPressure,HeartRate`

Your data processing pipeline must enforce the following rules for each row (excluding the header, which should be preserved exactly as is):

1. **Constraint-based Validation & Regex**:
   - Drop any row where `Age` is not a valid integer between 0 and 120 (inclusive).
   - Drop any row where `SSN` does not exactly match the standard US format: three digits, a hyphen, two digits, a hyphen, and four digits (e.g., `123-45-6789`).

2. **Data Masking and Anonymization**:
   - Redact the `Name` column by replacing its contents entirely with the string `REDACTED`.
   - Mask the `SSN` column to hide the first five digits, replacing them with asterisks but keeping the hyphens. For example, `123-45-6789` should become `***-**-6789`.

3. **Interpolation and Imputation**:
   - If the `BloodPressure` field is empty/missing, impute it with the default value `120/80`.
   - If the `HeartRate` field is empty/missing, impute it with the default value `72`.

Requirements:
- Your main script `/home/user/workflow.sh` should be executable.
- It must accept two arguments: the input directory and the output directory. Example usage: `./workflow.sh /home/user/raw_data /home/user/processed_data`
- The script must use parallel processing (e.g., `find ... | xargs -P 4 ...` or `parallel`).
- The processed files must retain their original filenames in the output directory.
- You may use standard Unix text processing tools (like `awk`, `sed`, `grep`, `bash`) to implement the logic. 

Please create and execute `/home/user/workflow.sh` on the provided raw data.