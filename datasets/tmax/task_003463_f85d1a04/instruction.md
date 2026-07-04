You are an automation specialist for a cold-chain logistics company. We have an incoming stream of temperature sensor logs mixed with driver notes, but our legacy systems are generating malformed data, and we suspect malicious injections in the driver notes field. 

Your objective is to build a robust data validation and processing pipeline.

**Step 1: Extract Configuration from Image**
We have a shipping configuration label located at `/app/config_label.png`. 
Use OCR (Tesseract is installed) to extract the text from this image. It contains three critical parameters in the format:
`WINDOW=<int> MAX_DEV=<float> ENCODING=<string>`
You must use these parameters in your validation script.

**Step 2: Create the Validator**
Write a Python module at `/home/user/validator.py` containing a function with the exact signature:
`def process_and_validate(filepath: str) -> bool:`

This function must do the following:
1. **Encoding Handling**: Open the file using the `ENCODING` extracted from the image. If the file cannot be decoded strictly with this encoding, return `False`.
2. **Parsing**: The file is a CSV with headers: `timestamp,temperature,notes`. (Timestamps are in ISO 8601 format).
3. **Resampling & Gap-Filling**: Parse the timeseries. Resample the data to a 1-minute frequency (`1T` or `1min`). For missing temperature values during resampling, use forward-filling (ffill).
4. **Rolling Statistics**: Calculate a rolling mean of the temperature using the `WINDOW` size extracted from the image. 
5. **Constraint-based Validation**: If any absolute deviation between a valid temperature reading and its corresponding rolling mean is strictly greater than `MAX_DEV`, return `False`. (Ignore `NaN` values in the rolling mean calculation for the first few rows before the window is full).
6. **Text Sanitization**: Examine the `notes` column. If any row's note contains the exact substrings `<script>` or `javascript:` (case-insensitive), return `False`.
7. Return `True` if the file passes all checks and processes successfully.

**Step 3: Pipeline Scheduling**
Create a bash script at `/home/user/pipeline.sh` that, when executed, echoes "Pipeline running". 
Configure a user cron job to execute `/home/user/pipeline.sh` every minute. Ensure the cron service is running or the crontab is properly installed for the `user` account.

**Output & Verification**
Our automated test suite will import `/home/user/validator.py` and run `process_and_validate()` against a secret corpus of "clean" and "evil" CSV logs. Your function must correctly identify and reject 100% of the evil logs while accepting 100% of the clean logs.