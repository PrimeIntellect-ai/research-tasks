You are a data analyst tasked with building a robust, reproducible data processing pipeline for a retail company. The company receives daily CSV drops of sales data, but the data quality is notoriously poor. 

You need to build a pipeline that enforces a strict data schema, aggregates the clean data deterministically, and includes a testing suite to guarantee pipeline reproducibility.

**Data Source**
Two batch files are located in `/home/user/raw_data/`:
1. `batch_A.csv`
2. `batch_B.csv`

The CSVs have the following headers: `id,category,price,quantity`

**Part 1: Data Schema & Pipeline Processing**
Create a script (in the language of your choice) named `/home/user/pipeline.py` (or `.sh`, `.R`, etc.) that takes two arguments: an input CSV path and an output directory path. 
Example usage: `python3 /home/user/pipeline.py /home/user/raw_data/batch_A.csv /home/user/processed/`

The pipeline must enforce the following schema rules row by row:
*   `id`: Must be exactly 8 alphanumeric characters.
*   `category`: Must be strictly one of `['Electronics', 'Clothing', 'Food']` (case-sensitive).
*   `price`: Must be a valid floating-point number strictly greater than or equal to `0.0`.
*   `quantity`: Must be a valid integer strictly greater than or equal to `1`.

Processing Rules:
1. If a row violates ANY of the schema rules, it must be completely excluded from aggregation.
2. The `id` of every excluded row must be appended to a file named `invalid_ids.txt` inside the output directory (one ID per line). If the file doesn't exist, create it.
3. For all valid rows, calculate the revenue: `revenue = price * quantity`.
4. Aggregate the total revenue by `category`.
5. Write the result to `aggregated.csv` in the output directory.
6. The `aggregated.csv` file must have exactly two columns: `category,total_revenue`.
7. The rows in `aggregated.csv` must be sorted alphabetically by `category`.
8. The `total_revenue` must be formatted to exactly two decimal places (e.g., `150.00`).

**Part 2: Reproducibility Testing**
To ensure the pipeline is fully reproducible and correctly handles bad data, write a bash script at `/home/user/test_reproducibility.sh`.

When run, this test script must automatically:
1. Clear out the `/home/user/processed/` directory.
2. Run your pipeline on `/home/user/raw_data/batch_A.csv`, outputting to `/home/user/processed/`.
3. Compute the SHA-256 hash of `/home/user/processed/aggregated.csv` and store it.
4. Delete the `/home/user/processed/` directory contents and re-run the pipeline on `batch_A.csv`.
5. Compute the SHA-256 hash of the newly generated `aggregated.csv`.
6. Compare the two hashes. If they do not match, the test fails.
7. Clear `/home/user/processed/` and run the pipeline on `/home/user/raw_data/batch_B.csv`.
8. Check if `/home/user/processed/invalid_ids.txt` contains exactly 4 lines (since `batch_B.csv` contains exactly 4 invalid rows). If it doesn't, the test fails.
9. If all tests pass, the script must write the exact string `REPRODUCIBILITY_PASS` to `/home/user/test_result.log`.

**Final Steps**
Run your testing script so that `/home/user/test_result.log` is generated. We will evaluate your solution by checking the contents of `/home/user/test_result.log` and running your pipeline against a hidden dataset.