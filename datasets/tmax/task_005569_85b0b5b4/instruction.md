You are an expert data analyst. We have a multi-source data processing pipeline that needs to be built and tested. 

Please perform the following steps:

1. **Analysis Environment Setup**:
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `pandas` in this virtual environment.

2. **Data Processing (ETL & Joining)**:
   - There are three CSV files located in `/home/user/data/`:
     - `sales.csv` (columns: `transaction_id`, `customer_id`, `amount`)
     - `customers.csv` (columns: `customer_id`, `region_id`)
     - `regions.csv` (columns: `region_id`, `region_name`, `tax_rate`)
   - Write a Python script at `/home/user/pipeline.py` (using the virtual environment's Python) that loads these three files.
   - Perform inner joins to combine the data: match `sales` to `customers` on `customer_id`, and then the result to `regions` on `region_id`.
   - Calculate a new column `tax_amount` which is exactly `amount * tax_rate`.
   - Aggregate the data to calculate the sum of `tax_amount` per `region_name`.
   - Save the aggregated results to `/home/user/output/aggregated_tax.csv`. The output CSV must have exactly two columns: `region_name` and `total_tax`, and should not include the row index.

3. **Experiment Tracking**:
   - During the execution of `pipeline.py`, you must compute some tracking metrics to verify the data integrity.
   - Save these metrics to a JSON file at `/home/user/experiment_log.json`.
   - The JSON file must have exactly the following keys:
     - `"total_sales_rows"`: Integer, the number of rows in the original `sales.csv` file.
     - `"valid_joined_rows"`: Integer, the number of rows remaining after completing all inner joins.
     - `"max_tax_region"`: String, the `region_name` that has the highest aggregated `total_tax`.

Run your script and ensure `/home/user/output/aggregated_tax.csv` and `/home/user/experiment_log.json` are generated successfully.