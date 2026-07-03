You are a data analyst tasked with building a reproducible ETL script to clean a noisy dataset of server metrics.

The raw data is located at `/home/user/raw_metrics.csv` and contains four columns: `timestamp`, `cpu_usage`, `memory_usage`, and `response_time`.

Please perform the following operations to clean the data:
1. Create a Python script at `/home/user/clean_metrics.py`.
2. The script must read `/home/user/raw_metrics.csv`.
3. First, calculate the median of the `memory_usage` column using all initially valid (non-null) values, and use this median to fill any missing (`NaN` or empty) values in the `memory_usage` column.
4. Next, filter out outliers: remove any rows where `cpu_usage` is strictly greater than `100.0` or strictly less than `0.0`.
5. Finally, drop any rows that still contain missing values in any column.
6. Save the cleaned dataset to `/home/user/clean_metrics.csv` (without the index column).

To ensure this pipeline is reproducible and properly isolates dependencies, you must also create a bash script at `/home/user/run_pipeline.sh` that:
1. Creates a Python virtual environment in `/home/user/venv`.
2. Activates the virtual environment.
3. Installs `pandas`.
4. Executes your `/home/user/clean_metrics.py` script.

Make sure `/home/user/run_pipeline.sh` is executable (`chmod +x`). 
Once you have created both files, run `/home/user/run_pipeline.sh` to produce the final `clean_metrics.csv`.