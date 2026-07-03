You are a data scientist working on an edge-computing project. You need to build a lightweight ETL pipeline using primarily Bash, as the edge devices do not have large data processing libraries installed. 

You have been given a raw, messy dataset at `/home/user/raw_sensor_data.csv`. The file has a header: `timestamp,sensor_id,temperature,humidity,status`.

Your task is to write a Bash script at `/home/user/etl_pipeline.sh` that performs the following data cleaning and preparation steps, and then triggers a hyperparameter tuning script.

**ETL Pipeline Requirements:**
1. **Data Schema Enforcement:** Read `/home/user/raw_sensor_data.csv` (skipping or preserving the header is up to you, but the output must have exactly the same header). Drop any rows that do not have exactly 5 comma-separated columns.
2. **Missing Value Handling:** If the `temperature` column (the 3rd column) is empty (e.g., `...,,,...`), impute it by replacing the empty value with `25.0`.
3. **Outlier Handling:** Drop any rows where the `humidity` column (the 4th column) is strictly less than `0.0` or strictly greater than `100.0`. (Assume humidity values are formatted as floats or ints).
4. **Save Cleaned Data:** Save the processed dataset (with header) to `/home/user/cleaned_sensor_data.csv`.
5. **Hyperparameter Tuning Integration:** After the data is cleaned, your bash script must execute the pre-existing Python script `/home/user/tune.py` passing the cleaned data file as its only argument. E.g., `python3 /home/user/tune.py /home/user/cleaned_sensor_data.csv`.

**Deliverables:**
1. Create and run `/home/user/etl_pipeline.sh`.
2. Ensure `/home/user/cleaned_sensor_data.csv` is correctly formatted.
3. The `tune.py` script will automatically generate `/home/user/best_model_metrics.json` upon successful execution.

**Note:** You must write the logic for schema enforcement, missing value imputation, and outlier removal purely in Bash/standard Unix utilities (like `awk`, `sed`, `grep`). Do not use Python to clean the data.