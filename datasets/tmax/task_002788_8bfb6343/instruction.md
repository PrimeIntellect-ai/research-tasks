You are a data engineer building an ETL pipeline to process acoustic sensor data. We have received a batch of sensor readings encoded as an audio file at `/app/sensor.wav`. 

Your task is to extract the time-series data from this audio file, clean it, and compute rolling statistics using only Bash, `awk`, `sox`, and other standard Linux CLI tools. 

Perform the following steps:
1. Extract the time and amplitude values from `/app/sensor.wav` into a plain text format (e.g., using `sox` with the `.dat` format).
2. Take the absolute value of the amplitude.
3. Constraint/Imputation: The sensor occasionally fails, outputting an amplitude of exactly `0.00000000`. Treat any exactly zero amplitude as a missing value and impute it by carrying forward the last seen non-zero absolute amplitude. (Assume the first sample is never zero).
4. Normalization: Normalize these imputed absolute amplitudes to a 0.0 to 1.0 scale by dividing by the maximum imputed absolute amplitude found in the entire dataset.
5. Rolling Statistic: Compute a 5-sample simple moving average (SMA) of the normalized values. For the first 4 samples, compute the average of whatever window is available (e.g., sample 1 is just sample 1; sample 2 is average of 1 and 2, etc.).
6. Save the final output as a CSV file at `/home/user/processed_signal.csv` with exactly two columns: `time` and `smoothed_normalized_amplitude`. Use a comma separator. Ensure the time column retains its original precision.

Do not use Python, R, or other scripting languages for the data processing pipeline; stick strictly to Bash and core utilities like `awk` and `sox`.