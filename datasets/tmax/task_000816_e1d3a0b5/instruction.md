You are acting as a log analyst investigating a failing data pipeline. The existing pipeline processes a large batch of system logs but has been silently dropping or corrupting records that contain multi-line messages (specifically, CSV rows containing embedded newlines in the `LogMessage` field).

Your goal is to build a robust Python data processing script that correctly parses the CSV, validates and extracts specific event data using a schema defined in an image, and outputs a sorted, clean dataset.

Here are the requirements:

1. **Input Data**: The raw logs are located at `/app/system_logs.csv`. This file has three columns: `SessionID`, `Timestamp` (ISO 8601), and `LogMessage`. Some `LogMessage` fields contain quoted strings with embedded newlines (e.g., stack traces).

2. **Target Schema**: We are only interested in a specific type of validation event embedded within the `LogMessage`. The exact Regex pattern you need to use to extract the `EventID` and `GateStatus` from the `LogMessage` is provided in an image located at `/app/target_pattern.png`. You will need to use OCR (e.g., `tesseract`, which is installed) to read this regex pattern. 
   - The regex contains two capture groups: Group 1 is the `EventID` and Group 2 is the `GateStatus`.

3. **Processing Requirements**:
   - Read `/app/system_logs.csv` properly, ensuring that rows with embedded newlines are NOT dropped or split incorrectly.
   - Filter the dataset to keep *only* the logs where the `LogMessage` matches the regex pattern found in the image.
   - Extract the `EventID` and `GateStatus` using the capture groups from the regex.
   - Group and sort the extracted records primarily by `SessionID` (ascending alphabetically) and secondarily by `Timestamp` (ascending chronological order).

4. **Output**:
   - Save the processed data to `/home/user/processed_logs.csv`.
   - The output CSV must contain exactly four columns with headers: `SessionID`, `Timestamp`, `EventID`, `GateStatus`.
   - Ensure the output is a valid CSV.

Your output will be evaluated by an automated script that calculates the F1-score of your extracted records against a hidden reference set. You must achieve a score of >= 0.95.