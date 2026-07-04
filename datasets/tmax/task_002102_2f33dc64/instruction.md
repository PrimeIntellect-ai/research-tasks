You are a data engineer tasked with optimizing an ETL pipeline based on a spoken request from a stakeholder.

We have a massive dataset of customer interactions and transactions located at `/home/user/data/interactions.csv`. 

Your tasks are:
1. **Transcribe the Audio Request**: A stakeholder has left a brief voice memo detailing which specific subset of data they need analyzed. The audio file is located at `/app/query.wav`. You will need to transcribe this audio to extract two key pieces of information: a `user_id` (an integer) and a `region_code` (a string).
2. **Develop an Efficient ETL Pipeline**: Write a Python script at `/home/user/fast_etl.py` that performs the following operations:
   - Reads `/home/user/data/interactions.csv`.
   - Filters the dataset for rows matching the `user_id` and `region_code` mentioned in the audio.
   - For the filtered rows, processes the `interaction_text` column: tokenizes the text by converting it to lowercase, removing all non-alphanumeric characters (except spaces), and splitting by whitespace.
   - Calculates the sum of the `transaction_amount` for this filtered subset.
   - Identifies the single most frequent token across all filtered `interaction_text` rows.
   - Outputs a JSON file to `/home/user/summary.json` with the exact keys: `"total_amount"` (float, rounded to 2 decimal places) and `"top_token"` (string).

**Performance Requirement:**
The CSV file contains over 1 million rows. A naive row-by-row Python implementation takes too long. Your script `/home/user/fast_etl.py` must complete the execution and output generation in under 2.0 seconds. You may use efficient libraries like `pandas`, `duckdb`, or `polars` which are standard in data science environments.

Ensure your code is clean and executable via `python /home/user/fast_etl.py`.