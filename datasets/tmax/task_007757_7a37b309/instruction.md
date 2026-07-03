You are a data engineer tasked with building a robust, parallelized ETL pipeline for processing IoT telemetry data.

We have a set of raw CSV files coming from various regions, located in `/home/user/telemetry_input/`. 

Your goal is to write a Python script at `/home/user/etl_pipeline.py` and run it to process these files. The script must meet the following requirements:

1. **Parallel Processing**: You must use Python's `multiprocessing` module (e.g., `Pool` or `Process`) to read and process the CSV files in `/home/user/telemetry_input/` in parallel.
2. **Data Normalization**: 
   - The input CSVs have the headers: `timestamp,sensor_id,metric_type,value,unit`
   - If `metric_type` is `temp` and `unit` is `F`, you must convert the `value` to Celsius (`C`) using the formula `(F - 32) * 5/9` and change the unit to `C` in memory.
3. **Constraint-based Validation (Quality Gates)**:
   - For `temp` (after converting to Celsius), valid values are between `-50` and `60` inclusive.
   - For `humidity`, valid values are between `0` and `100` inclusive.
   - Any row that violates these constraints, or cannot be parsed as a float, must be rejected.
4. **Sorting and Grouping**:
   - For all valid records, group the data by `sensor_id` and `metric_type`.
   - Calculate the average `value` for each group.
   - Sort the final grouped results alphabetically first by `sensor_id`, then by `metric_type`.
5. **Output**:
   - Create a directory `/home/user/etl_output/`.
   - Save the valid, aggregated results to `/home/user/etl_output/aggregated.json`. The JSON should be a list of objects in this exact format, with averages rounded to 2 decimal places:
     `[{"sensor_id": "S1", "metric_type": "temp", "avg_value": 22.00}, ...]`
   - Save all rejected rows (exactly as they appeared in the input, keeping original headers) to `/home/user/etl_output/rejected_records.csv`.

Write the script, execute it, and ensure the output files are generated correctly.