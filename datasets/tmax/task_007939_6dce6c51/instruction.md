You are a data analyst tasked with building a robust, multi-stage data processing pipeline to handle a continuous stream of e-commerce transactions. 

Currently, our transaction logs are stored in a messy CSV file at `/home/user/transactions.csv`. We also have a JSON file containing fixed exchange rates at `/home/user/exchange_rates.json`.

Your objective is to orchestrate a pipeline that streams this data over a local HTTP service, standardizes the messy fields on the fly, and aggregates the results into a daily summary report.

Here are your specific instructions:

1. **Serve the Data**: Use Python's built-in `http.server` to serve the directory `/home/user/` on port `8080` in the background. This simulates an internal data endpoint.

2. **Stream and Process**: Write a Python script at `/home/user/process_pipeline.py` that reads the CSV data from `http://localhost:8080/transactions.csv` using a streaming HTTP request. You must process the data line-by-line or in chunks to minimize memory usage (do not load the entire file into memory).

3. **Normalization Rules**:
    As you process each row, apply the following standardizations:
    * `timestamp`: The input contains timestamps in various formats (e.g., `MM/DD/YYYY HH:MM:SS`, `YYYY-MM-DDTHH:MM:SSZ`, `DD-MM-YYYY HH:MM`). Convert them all to a standard `YYYY-MM-DD` date string representing the UTC date.
    * `email`: Lowercase the email address and remove any leading or trailing whitespace. Ignore rows where the email is completely empty.
    * `amount` and `currency`: Convert the transaction `amount` to a new field `amount_usd` using the rates in `/home/user/exchange_rates.json`. If a currency is not found in the JSON file, drop the row.

4. **Aggregation**:
    Calculate the total `amount_usd` (sum) for each unique `YYYY-MM-DD` date.

5. **Output**:
    Write the final aggregated data to `/home/user/daily_summary.json`. 
    The JSON file should be a dictionary where the keys are the `YYYY-MM-DD` date strings and the values are the total `amount_usd` rounded to exactly 2 decimal places (as floats).

Run your pipeline so that `/home/user/daily_summary.json` is generated.