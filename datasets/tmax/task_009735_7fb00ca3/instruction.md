You are helping a data scientist clean and process a dataset of sensor readings. 

There is a remote data server simulated locally on port `8080`. 
Your tasks are:
1. Download two files from `http://localhost:8080/`:
   - `sensor_log.csv`: A CSV file containing sensor readings with columns `timestamp,sensor_id,value`.
   - `report_template.md`: A markdown template file for the final report.
2. Using Bash tools (like `awk`, `sed`, `grep`, etc.), calculate the 3-point rolling average for each `sensor_id` in the dataset. The data is already sorted chronologically. You need to find the *latest* (final) 3-point rolling average for each sensor. If a sensor has fewer than 3 readings, calculate the average of however many readings it has.
3. The template file contains placeholders in the format `{{SENSOR_ID_AVG}}` (e.g., `{{S1_AVG}}`). Replace these placeholders with the calculated final rolling averages, formatted to exactly one decimal place.
4. Save the generated report to `/home/user/final_report.md`.

Ensure you rely strictly on shell scripting (Bash, Awk, Sed, etc.) and do not use Python or other high-level languages for the data processing.