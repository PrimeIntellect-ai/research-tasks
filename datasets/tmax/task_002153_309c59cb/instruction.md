As a localization engineer, you are tracking the usage metrics of translation strings across different regions to prioritize the upcoming localization updates. You have received a time series export of string access logs, but the data pipeline that produced it had occasional drops, resulting in missing access count values.

Your task is to build a robust C-based data processing tool and a Bash pipeline wrapper to clean this time series data.

**Data Details:**
The input file is located at `/home/user/raw_metrics.csv`.
It has four columns: `timestamp,locale,string_id,access_count`
- `timestamp`: Unix epoch time (integer)
- `locale`: e.g., "es-ES", "fr-FR" (string)
- `string_id`: e.g., "ui.button.save" (string)
- `access_count`: Integer representing hits, or MISSING (represented by an empty string, e.g., `1672531260,es-ES,ui.button.save,`).

**Requirements:**

1. **C Program (`/home/user/impute_loc.c`):**
   - Write a C program that reads `raw_metrics.csv` from the current directory.
   - It must parse the CSV and impute any missing `access_count` values using **Last Observation Carried Forward (LOCF)**. 
   - Note: The LOCF must be tracked *independently* for each unique combination of `locale` and `string_id`.
   - If the very first observation for a given `locale` and `string_id` pair is missing, impute it with `0`.
   - Write the cleaned data to `/home/user/clean_metrics.csv` in the exact same format (`timestamp,locale,string_id,access_count`), preserving the original row order.

2. **Pipeline Wrapper (`/home/user/run_pipeline.sh`):**
   - Write a Bash script that automates the workflow.
   - It must compile the C program using `gcc` into an executable named `impute_loc`.
   - It must execute `./impute_loc`.
   - It must implement pipeline logging by writing to `/home/user/pipeline.log`. 
     - Before compiling: append `[INFO] Starting localization metrics pipeline`
     - Upon successful execution of the C program: append `[SUCCESS] Clean metrics generated`
     - If compilation or execution fails, append `[ERROR] Pipeline failed` and exit with a non-zero status.

Ensure all files are created in `/home/user` and the bash script has executable permissions.