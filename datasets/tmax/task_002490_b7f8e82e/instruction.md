You are an ML engineer preparing training data for a new model. 

We have a simple data processing script located at `/home/user/process.py`. It reads a raw CSV dataset from `/home/user/data/raw_data.csv` and outputs a Parquet file to `/home/user/processed.parquet`. 

Currently, the downstream training pipeline is crashing due to a schema enforcement error. The columns `user_id` and `group_id` are supposed to be strictly integers. However, because the raw CSV contains missing values (empty strings) in these columns, pandas is silently upcasting them to `float64` via NaN introduction. This breaks the expected integer schema and causes numerical accuracy issues for our ID hashing functions.

Your task is to:
1. Modify `/home/user/process.py` so that it uses pandas' nullable integer data type (`Int64`) for any column that ends with `_id`, preventing them from being cast to floats.
2. Run the updated script to successfully generate `/home/user/processed.parquet` with the correct schema.
3. Create a text file at `/home/user/fixed_columns.txt` containing the exact names of the columns you fixed, one per line, sorted alphabetically.

The system relies on you using standard Python tools (like pandas) and bash commands to complete this short task.