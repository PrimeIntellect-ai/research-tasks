You are a data scientist cleaning up a messy IoT dataset. 
A previous pipeline attempted to parse this data but failed because the `Data` column contains embedded newlines inside quoted CSV fields, causing standard line-by-line tools to break. 

Your task is to write a Go program `/home/user/process.go` (using only the standard library) that reads `/home/user/raw.csv` and produces a cleaned, reshaped, and aggregated dataset at `/home/user/clean.csv`.

Here are the requirements for your Go program:

1. **Parse the CSV:** Read `/home/user/raw.csv`. The file has headers: `Time,Station,Data`. The `Data` column contains multiline strings with sensor readings (e.g., `Temp: 20.5\nHum: 50.0`).
2. **Information Extraction & Reshaping (Wide to Long):** Extract the `Temp` and `Hum` (Humidity) float values from the `Data` column. Reshape this data so that each row represents a single metric. The target columns are `Time` (int), `Station` (string), `Metric` (string, either `Temp` or `Hum`), `Value` (float), and `RollAvg` (float). 
3. **Imputation:** Because sensors sometimes fail to report, some metrics might be missing for a given `Time` and `Station`. 
    - If a metric is missing, use **forward-fill** (use the most recent previous `Value` for that specific `Station` and `Metric`, ordered by `Time`). 
    - If the *first* time period (Time=1) is missing a metric for a station, impute it with `0.0`.
4. **Windowed Aggregation:** Calculate a rolling average for each `Station` and `Metric` with a window size of **2** (the current imputed value and the previous imputed value). If there is no previous value (i.e., at Time=1), the rolling average is just the current value.
5. **Formatting:** Output to `/home/user/clean.csv`. Include the header `Time,Station,Metric,Value,RollAvg`. Sort the output primarily by `Station` (alphabetically), then by `Metric` (alphabetically), and finally by `Time` (ascending). Format all floats to exactly one decimal place.

Run your Go program to generate `/home/user/clean.csv` before finishing the task.