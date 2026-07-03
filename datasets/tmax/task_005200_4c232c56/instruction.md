You are a data engineer tasked with building an ETL pipeline in Go to fuse irregular data from two IoT sensors. 

You have been provided with two input files in `/home/user/data/`:
1. `temperature.csv` - Contains irregular temperature readings.
   Format: `timestamp,temperature`
2. `pressure.csv` - Contains regular but sometimes missing pressure readings.
   Format: `timestamp,pressure`

Your goal is to write a Go program at `/home/user/process.go` that processes these files and produces a unified, cleaned dataset at `/home/user/output.csv`.

Here are the exact processing requirements:
1. **Timestamp Alignment & Union**: Determine the earliest and latest timestamps across BOTH files (truncated to the minute). Generate a continuous minute-by-minute time series from the minimum minute to the maximum minute inclusive.
2. **Aggregation**: For each minute in the continuous series, aggregate the raw readings from both files. If there are multiple readings in the same minute for a sensor, take the arithmetic mean. If there are no readings, the aggregated value is considered missing.
3. **Imputation (Pressure)**: For any missing aggregated pressure values, perform a **linear interpolation** using the nearest prior and subsequent available aggregated pressure values in the continuous series. (Assume the first and last minutes in the overall series will always have or be provided with a valid pressure reading, so no extrapolation is needed).
4. **Imputation (Temperature)**: For any missing aggregated temperature values, perform a **forward-fill** (use the most recent available aggregated temperature). Assume the first minute always has a temperature reading.
5. **Windowed Aggregation**: Compute a 5-minute rolling average of the forward-filled temperature. For a given minute `T`, the rolling average is the mean of the temperatures at `T, T-1, T-2, T-3,` and `T-4`. If fewer than 5 minutes of history exist (i.e., near the start of the series), calculate the average using only the available history up to that point.
6. **Output**: Write the results to `/home/user/output.csv` with the following exact headers: `timestamp,temp_filled,pressure_interpolated,temp_rolling_avg`.
   - `timestamp` must be in RFC3339 format (e.g., `2023-10-01T10:00:00Z`).
   - Float values must be formatted to exactly two decimal places (e.g., `20.50`).

To successfully complete the task, write the Go script, run it to generate the output file, and ensure the output matches the requirements. Standard library packages are preferred, but if you need external packages, use `go mod init` and `go get`.