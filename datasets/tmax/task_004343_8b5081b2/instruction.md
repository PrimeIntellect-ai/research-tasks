You are tasked with building a robust data processing pipeline for a configuration management system. We have several servers that dump their configuration change events into CSV files. These files contain raw configuration diffs that span multiple lines, meaning the CSV fields have embedded newlines. A naive line-by-line parser will fail or silently drop/corrupt rows.

Your goal is to write a Python script `/home/user/process_configs.py` that processes these files, extracts features, calculates rolling statistics, and validates the output. 

Here are the requirements for your script:

1. **Input Location**: Read all `.csv` files from `/home/user/raw_data/`. The files have the following columns: `event_id,timestamp,server_id,service_name,config_diff`.
2. **Parallel Feature Extraction**: Read the files and extract features in parallel (using Python's `multiprocessing` or `concurrent.futures`). When parsing, ensure you correctly handle embedded newlines in the `config_diff` field. For each row, calculate a new feature: `diff_line_count` (the number of lines in `config_diff`). For example, a string `"line1\nline2"` has 2 lines. Empty strings have 0 lines.
3. **Pipeline DAG / Aggregation**: Combine the extracted records from all files into a single dataset. Sort the combined dataset primarily by `timestamp` (ascending) and secondarily by `event_id` (ascending).
4. **Rolling Statistics**: Group the sorted dataset by `service_name`. For each group, calculate a rolling average of the `diff_line_count` over a window of the current event and up to 2 previous events (maximum window size of 3, minimum periods of 1). Name this new column `rolling_avg_diff`. Round this value to exactly 2 decimal places.
5. **Validation Checkpoints**: Implement a validation function that runs before saving. It must check that:
    - There are no missing (null/NaN) values in `diff_line_count` or `rolling_avg_diff`.
    - Every row has a `rolling_avg_diff` >= 0.
    If validation fails, the script should print an error and exit with a non-zero status code.
6. **Output**: Save the final validated dataset to `/home/user/output/final_stats.csv`. The output CSV must contain exactly these columns in this order: `event_id,timestamp,server_id,service_name,diff_line_count,rolling_avg_diff`. 

The system already has Python 3 and `pandas` installed. You should create the `/home/user/output/` directory if it does not exist. Run your script to produce the final output file.