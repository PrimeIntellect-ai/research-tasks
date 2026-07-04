You are an automation specialist tasked with building a robust data processing workflow for an international IoT sensor network. 

The system receives raw sensor logs in a CSV file, but the data is messy: it has missing values, mixed scales, and occasional extreme anomalies. Moreover, the logs contain multilingual event descriptions in UTF-8 that must be preserved.

Your task is to write a C program (`/home/user/process_ts.c`) and a bash orchestration script (`/home/user/workflow.sh`) to clean, analyze, and standardize this time-series data.

**Input Data:**
A raw log file will be located at `/home/user/raw_sensors.csv`.
It has three columns: `Timestamp,EventMessage,Value`
Example rows:
```
1620000000,正常,10.0
1620000060,警告,
1620000120,ok,14.0
```
Notice that the second row is missing a value. Missing values are represented by empty strings after the last comma. 

**Requirements for the C Program (`/home/user/process_ts.c`):**
1. **Read & Parse:** Read the CSV line by line. Preserve the UTF-8 `EventMessage` exactly as is.
2. **Imputation:** For any missing `Value`, perform linear interpolation using the nearest preceding and succeeding valid values. (Assume the first and last rows of the file will always have valid values).
3. **Standardization:** Calculate the population mean and population standard deviation of the *interpolated* dataset. Then, calculate the Z-score for every row: `Z = (Value - Mean) / StdDev`.
4. **Anomaly Detection:** Flag a row as an anomaly (`1`) if its absolute Z-score is strictly greater than `2.0`. Otherwise, flag it as `0`.
5. **Output:** The C program should print the processed data to standard output in the following CSV format:
`Timestamp,EventMessage,InterpolatedValue,ZScore,IsAnomaly`
Use `%.4f` for both `InterpolatedValue` and `ZScore`.

**Requirements for the Bash Script (`/home/user/workflow.sh`):**
1. Compile the C program to `/home/user/process_ts` using `gcc` with standard mathematical libraries (`-lm`).
2. Execute the compiled program, feeding it `/home/user/raw_sensors.csv`.
3. Save the standard output of the C program to `/home/user/processed_sensors.csv`.

**Constraints:**
- You may only use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`).
- Do not hardcode the number of rows; read dynamically until EOF.
- The `workflow.sh` script must be executable (`chmod +x`).

Complete the task by ensuring `/home/user/processed_sensors.csv` is correctly generated.