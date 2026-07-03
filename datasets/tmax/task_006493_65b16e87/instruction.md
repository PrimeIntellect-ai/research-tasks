You are a data engineer responsible for a critical ETL pipeline. We have a set of raw temperature sensor logs in multiple formats (CSV and JSON) stored in `/home/user/sensor_logs/`. 

Your task is to write a Python script that reads all the data, detects anomalies, and generates an HTML report using a provided Jinja2 template.

Here are the specific requirements:
1. Read all `.csv` and `.json` files in `/home/user/sensor_logs/`.
   - CSV files have columns: `timestamp`, `sensor_id`, `temperature`.
   - JSON files contain a list of objects, each with keys: `timestamp`, `sensor_id`, `temperature`.
2. Consolidate the data and calculate the global mean and standard deviation of the `temperature` for **each** `sensor_id` across all files.
3. Flag any reading as an anomaly if its temperature is strictly greater than 2 standard deviations away from the mean for its respective `sensor_id` (i.e., `abs(temp - mean) > 2 * std_dev`). Use sample standard deviation (ddof=1).
4. Use the Jinja2 template provided at `/home/user/report_template.j2` to generate an HTML report. The template expects a variable named `anomalies`, which should be a list of dictionaries with keys: `timestamp`, `sensor_id`, and `temperature`, sorted chronologically by `timestamp` (ascending).
5. Save the generated HTML to `/home/user/anomaly_report.html`.

Notes:
- You may need to install standard Python data engineering packages (like `pandas` and `jinja2`) to complete this task.
- Ensure your output file is placed exactly at `/home/user/anomaly_report.html`.