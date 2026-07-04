You are an AI assistant tasked with processing configuration management logs to track system configuration drift.

We have exported legacy configuration tracking logs into a file located at `/home/user/raw_configs.csv`. Because it comes from a legacy Windows-based configuration manager, the file is encoded in `UTF-16LE`.

The dataset is currently in a wide format. Each row represents a daily snapshot of the configuration. The columns are:
- `Date` (format: YYYY-MM-DD)
- Various microservice parameters in the format `<ServiceName>_<ParameterName>` (e.g., `AuthService_Timeout`, `AuthService_MemoryLimit`, `PaymentService_Timeout`, etc.)

Your task is to write and execute a Python script (`/home/user/process_drift.py`) to process this file into a validated, long-format dataset. The script must perform the following pipeline:

1. **Character Encoding Handling**: Read `/home/user/raw_configs.csv` correctly using `UTF-16LE` encoding.
2. **Wide-to-Long Reshaping**: Melt the dataset so that each row represents a single configuration parameter for a specific service on a given date. The resulting DataFrame should have four columns: `Date`, `Service`, `Parameter`, and `Value`. (Extract `Service` and `Parameter` by splitting the original column names at the underscore `_`).
3. **Rolling Statistics**: Group the data by `Service` and `Parameter`, sort chronologically by `Date`, and compute a 3-day rolling average (window size = 3, min_periods = 3) of the `Value`. Store this in a new column called `RollingAvg`.
4. **Validation Checkpoints (Quality Gate)**: Filter the resulting dataset. You must DROP any rows that meet ANY of the following conditions:
   - `RollingAvg` is null/NaN (which will be the case for the first two days of any group).
   - For any `Parameter` equal to `Timeout`, drop the row if `RollingAvg > 1000`.
   - For any `Parameter` equal to `MemoryLimit`, drop the row if `RollingAvg > 8192`.
5. **Output**: Save the final filtered DataFrame to `/home/user/validated_configs.csv`. It must be saved in `UTF-8` encoding, containing only the columns `Date`, `Service`, `Parameter`, `Value`, and `RollingAvg`. Round the `RollingAvg` to 2 decimal places. Sort the final output primarily by `Service` (ascending), then by `Parameter` (ascending), and finally by `Date` (ascending). Do not include the DataFrame index in the CSV.

Run your script to produce `/home/user/validated_configs.csv`.