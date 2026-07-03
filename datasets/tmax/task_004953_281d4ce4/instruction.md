You are a data engineer tasked with repairing a broken ETL package and building a feature processing pipeline for a downstream machine learning system. 

We have vendored a local copy of the `tablib` package at `/app/tablib-0.14.0`. However, a recent configuration change broke its installation process (a deliberate perturbation in the setup environment), causing it to fail when processing datasets with mixed types. Your first task is to identify the issue in the vendored package's build/install configuration, fix it, and install the package correctly in your environment.

After fixing the package, you must write an ETL script named `/home/user/etl_pipeline.py`. This script will be tested against a strict automated verifier that feeds it random generated datasets. Your script must behave EXACTLY like our reference implementation.

The script `/home/user/etl_pipeline.py` must take two positional arguments:
1. `input_csv_path`: Path to an input CSV containing sales data.
2. `input_json_path`: Path to an input JSON file containing product metadata.

The script must perform the following operations exactly:
1. Read both datasets using the repaired `tablib` package.
2. Join the sales data and product metadata on the `product_id` column (inner join).
3. Handle missing values: Fill any missing integer quantities with `0` (ensure they remain integers and are not silently cast to floats via NaN introduction).
4. Feature Engineering: Create a new column `total_value` = `quantity` * `price`.
5. Dimensionality Reduction / Linear Algebra: Extract the numeric columns (`quantity`, `price`, `total_value`). Compute the covariance matrix of these three columns (unbiased, ddof=1).
6. Flatten the covariance matrix and print the values as a comma-separated string to `stdout`, formatted to 4 decimal places.

Your script will be tested using a fuzz-equivalence verifier. It will be run hundreds of times with random CSV and JSON files, and its standard output must perfectly match the hidden oracle.

Constraints:
- Do not use `pandas` or `numpy` for the data ingestion or join; you must use the repaired `tablib` package to load the data. You may use `numpy` for the covariance matrix calculation.
- The output format must be strictly: `val1,val2,val3,val4,val5,val6,val7,val8,val9` printed to standard output.
- All code must be in `/home/user/etl_pipeline.py` and executable via `python3 /home/user/etl_pipeline.py <csv> <json>`.