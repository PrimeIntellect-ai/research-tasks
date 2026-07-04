You are a data analyst debugging a data processing pipeline. 

You have been provided with a dataset at `/home/user/measurements.csv` containing environmental sensor data. The format is: `timestamp,sensor_name,value`. 
For example:
```
2023-10-01T12:00:00,Alpha,23.5
2023-10-01T12:01:00,Beta,-2.1
2023-10-01T12:02:00,Alpha,
```

There is an existing Bash script at `/home/user/analyze.sh` intended to parse this file, compute the average value for each sensor, and generate an ASCII bar chart. However, the script is currently failing and producing a blank or erroneous report. It suffers from a few key issues:

1. **Numerical/Environment Configuration:** The script relies on standard CLI tools for math, but it suffers from severe precision loss and syntax errors. You will need to either configure the tools correctly (e.g., setting the right environment variables or flags for floating-point arithmetic) or refactor the calculation block to process decimals robustly.
2. **Missing Values:** The dataset contains missing values (represented as empty strings for the `value` field). The current script tries to process these blindly, causing calculation errors. You must filter out any row with a missing value.
3. **Outliers:** Due to sensor malfunctions, there are anomalous readings. Any row where the `value` is less than `-10.0` or greater than `50.0` is an outlier and must be excluded from the analysis.

Your task is to fix `/home/user/analyze.sh` (or rewrite it entirely in Bash) so that it successfully performs the data processing and writes its final output to `/home/user/sensor_report.txt`.

The final `/home/user/sensor_report.txt` must meet these exact specifications:
- One line per unique sensor found in the dataset, sorted alphabetically by sensor name.
- Format for each line: `Sensor: <sensor_name> | Avg: <average_value> | Plot: <asterisks>`
- `<average_value>` must be rounded to exactly two decimal places (e.g., `23.45`, `5.00`).
- `<asterisks>` is a string of `*` characters representing an ASCII bar chart. The number of asterisks must equal the floor of the average value (the integer part). For example, an average of `12.8` gets `12` asterisks. An average of `-2.1` gets `0` asterisks (empty plot string).

Run your script to ensure `/home/user/sensor_report.txt` is generated correctly.