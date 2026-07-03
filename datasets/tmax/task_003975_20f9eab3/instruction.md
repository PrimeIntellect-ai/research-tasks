You are a log analyst investigating patterns in a server's performance metrics. You have been provided with a CSV file at `/home/user/system_metrics.csv` containing server telemetry data in a "wide" format.

Your task is to write a C++ program that processes this data to identify anomalous metric spikes. You must follow this strict pipeline:

1. **Wide-Long Format Reshaping**: Parse the CSV and reshape the data from wide format (`timestamp,cpu,memory,disk`) into a long format. Each reshaped record should represent a single observation containing `timestamp`, `metric` (name of the metric as a string), and `value` (as a double).
2. **Validation Checkpoints (Quality Gate)**: Sometimes the logging agent corrupts data and outputs negative values. Implement a validation gate that drops any long-format record where `value < 0.0`. Do not process or include these invalid records in subsequent statistical calculations.
3. **Anomaly Detection**: For each distinct metric type (`cpu`, `memory`, `disk`):
   - Calculate the global Mean ($\mu$) of all valid values for that metric.
   - Calculate the Population Standard Deviation ($\sigma$) of all valid values for that metric. Note: Use Population Standard Deviation ($N$ in the denominator), not Sample Standard Deviation ($N-1$).
   - Identify any record as an anomaly if its value deviates from the mean by strictly more than 2 standard deviations: $|value - \mu| > 2\sigma$.
4. **Output**: Write the identified anomalies to a new CSV file at `/home/user/anomalies.csv`. 
   - Include a header row: `timestamp,metric,value`.
   - Print the `value` rounded to exactly 1 decimal place (e.g., `95.0`).
   - Order the rows primarily by `timestamp` (ascending) and secondarily by `metric` name (alphabetical).

You must write your solution in C++ and compile/run it in the terminal to produce the final `anomalies.csv` file. You may use standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<sstream>`, `<vector>`, `<map>`, `<cmath>`, `<iomanip>`).