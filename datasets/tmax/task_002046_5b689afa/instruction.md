You are a data engineer working on our machine learning platform. We have an ETL pipeline that prepares data for inference, but we are experiencing a data schema enforcement issue. 

Currently, the script `/home/user/etl_pipeline.py` reads raw feature data from `/home/user/raw_data.csv` and saves it as a Parquet file at `/home/user/processed_data.parquet`. However, the `click_count` column, which should exclusively represent integer counts, contains some missing values (NaNs). Because of pandas' default behavior, the entire `click_count` column is being silently cast to `float64`. This downstream schema violation crashes our strict inference benchmarking tool.

Your task is to:
1. Modify `/home/user/etl_pipeline.py` to enforce the correct schema. You must ensure that the `click_count` column is explicitly converted to pandas' nullable integer data type (`Int64`) before saving the Parquet file.
2. Execute the fixed `/home/user/etl_pipeline.py` to generate `/home/user/processed_data.parquet`.
3. Run the inference benchmarking tool by executing `/home/user/benchmark.py`. This script will verify the schema, simulate inference to track performance, and log the experiment tracking metrics to `/home/user/experiment_results.json`.

The task is successfully completed when the schema is correct, the pipeline runs without errors, and `/home/user/experiment_results.json` is successfully generated with the "success" status.