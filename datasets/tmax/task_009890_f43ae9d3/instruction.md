You are a Data Analyst at a global e-commerce company. You have been handed a large batch of raw sales data scattered across multiple CSV files and asked to generate a consolidated, standardized summary report.

The raw data is located in `/home/user/raw_data/` and consists of 20 CSV files (named `sales_chunk_0.csv` through `sales_chunk_19.csv`). 
Each CSV file has the following columns:
- `order_id` (string)
- `timestamp` (string)
- `category` (string)
- `price` (float)
- `quantity` (int)
- `currency` (string)

Additionally, there is an exchange rate configuration file located at `/home/user/config/exchange_rates.json` containing a mapping of currency codes to their USD conversion rate (e.g., `{"USD": 1.0, "EUR": 1.10, ...}`).

Your task is to write a Python script at `/home/user/process_sales.py` that does the following:
1. Installs any necessary dependencies (you may use standard tools like `pip`).
2. Reads all 20 CSV files **in parallel** (you must use a parallel processing approach, such as `concurrent.futures`, `multiprocessing`, `dask`, or similar, to read and process the files).
3. Calculates the `revenue_usd` for each row. The formula is: `revenue_usd = price * quantity * exchange_rate`. 
4. Aggregates the data to compute the `total_revenue_usd` and `total_items` (sum of quantity) sold for each unique `category`.
5. Sorts the aggregated data in **descending order** based on `total_revenue_usd`. In case of a tie, sort alphabetically by `category`.
6. Writes the final aggregated results into two different file formats in the `/home/user/processed/` directory (you must create this directory):
   - `/home/user/processed/summary.json`: A JSON array of objects. Example format:
     `[{"category": "Electronics", "total_revenue_usd": 150000.5, "total_items": 3500}, ...]`
     *(Note: Round `total_revenue_usd` to exactly 2 decimal places in the JSON output).*
   - `/home/user/processed/summary.parquet`: A Parquet file containing the exact same summary data (schema: `category` (string), `total_revenue_usd` (float), `total_items` (int)).

Ensure your script is fully self-contained and runs without errors. Run your script to generate the final output files.