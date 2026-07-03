You are a data scientist tasked with cleaning and transforming a raw, multi-language dataset of entity metrics. 

You have been provided with a raw dataset at `/home/user/raw_data.csv` which contains the following columns:
- `date`: The date of the record (YYYY-MM-DD)
- `entity_id`: An identifier for the entity (string)
- `text`: A text snippet that may contain various Unicode characters, multi-language text, and emojis.
- `daily_score`: A float representing a daily metric.

Your goal is to process this data using Python and load it into a SQLite database. Perform the following steps:

1. **Text Processing**: For each row, calculate the number of non-ASCII characters in the `text` field. Name this new feature `non_ascii_count`.
2. **Rolling Statistics**: Compute a 3-row rolling average of the `daily_score` for each `entity_id`. The data should be sorted by `date` ascending. The window should include the current row and up to 2 preceding rows for that `entity_id`. Round the result to 2 decimal places. Name this new feature `rolling_avg_score`.
3. **Data Export**: Save the transformed data (containing ONLY the columns: `date`, `entity_id`, `non_ascii_count`, `rolling_avg_score`) to a CSV file at `/home/user/cleaned_data.csv`. Include the header.
4. **Database Bulk Import**: Create a SQLite database at `/home/user/metrics.db`. Create a table named `entity_metrics` and bulk import the contents of `/home/user/cleaned_data.csv` into this table. Ensure the column names match the CSV headers exactly and that the data types are appropriately handled (date as text, entity_id as text, non_ascii_count as integer, rolling_avg_score as real).

You must write a Python script (e.g., `/home/user/process.py`) to handle the data transformations and use any standard tools (Python's sqlite3 or the sqlite3 CLI) to handle the database creation and import. 

When you have finished, ensure that the file `/home/user/metrics.db` exists and contains the populated `entity_metrics` table.