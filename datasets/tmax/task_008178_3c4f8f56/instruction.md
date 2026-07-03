You are a data engineer tasked with building a mini ETL pipeline to process IoT sensor data. 

You have been provided with two CSV files containing raw sensor readings:
1. `/home/user/temperature.csv` - Contains columns: `timestamp`, `device_id`, `temp_c`
2. `/home/user/humidity.csv` - Contains columns: `timestamp`, `device_id`, `humidity_pct`

Your task is to write and execute a Python script `/home/user/etl_pipeline.py` that performs the following steps in a sequential pipeline:

**1. Extract and Join:**
Read both CSV files and perform an inner join on `timestamp` and `device_id`. 

**2. Transform (Windowed Aggregation):**
Ensure the data is sorted by `device_id` and then by `timestamp` in ascending order.
For each unique `device_id`, calculate a 3-period rolling average of the `temp_c` column. 
- Use a minimum of 1 period for the rolling window (i.e., the first row will just be its own value, the second will be the average of the first two, etc.).
- Name this new column `rolling_temp_c`.
- Round the `rolling_temp_c` values to 2 decimal places.

**3. Transform (Feature Extraction):**
Create a new integer column named `high_risk`. 
- Set `high_risk` to `1` if BOTH `rolling_temp_c` > 30.0 AND `humidity_pct` > 70.0.
- Otherwise, set `high_risk` to `0`.

**4. Load:**
Save the resulting DataFrame to `/home/user/output.csv`. 
The final CSV must contain exactly these columns in this order:
`timestamp`, `device_id`, `temp_c`, `humidity_pct`, `rolling_temp_c`, `high_risk`

Do not include the dataframe index in the output CSV. You may use `pandas` to accomplish this task. Ensure you install any necessary libraries if they are not present.