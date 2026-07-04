As an automation specialist, you are tasked with creating a log processing workflow that parses raw system logs, extracts features, calculates summary statistics, and outputs the results in multiple formats for downstream analysis.

You have been provided with a raw log file in CSV format at `/home/user/raw_logs.csv`.

Your goal is to write and execute a Python script at `/home/user/process_logs.py` that performs the following steps:

1. **Read and Filter**: Read `/home/user/raw_logs.csv`. Filter the data to include only rows where the `log_message` contains the string `"ERROR:"` (case-sensitive).
2. **Feature Extraction & Normalization**: For each error row, extract the text that appears *after* `"ERROR: "`. Tokenize this text into words. Normalize the words by converting them to lowercase and removing all punctuation (keep only alphanumeric characters `a-z` and `0-9`).
3. **Aggregation**: For each `server_id`, calculate:
   - The total number of error log lines (`total_errors`).
   - The frequency of each normalized word across all error messages for that server.
   - The most frequent word (`top_word`) and its count (`top_word_count`). If there is a tie for the highest count, select the word that comes first lexicographically (alphabetically).
4. **Multi-format Output**:
   - **JSON Summary**: Export the summary statistics to `/home/user/summary.json`. The file should contain a JSON array of objects, one for each server, sorted alphabetically by `server_id`. Each object must have the exact keys: `"server_id"` (string), `"total_errors"` (integer), `"top_word"` (string), and `"top_word_count"` (integer).
   - **Parquet Details**: Export the complete word frequency data to `/home/user/word_counts.parquet`. The Parquet file must have the schema: `server_id` (string), `word` (string), `count` (integer). The rows must be sorted by `server_id` (ascending), then by `count` (descending), and finally by `word` (ascending).

Make sure to install any necessary Python packages (like `pandas` and `pyarrow`) if they are not already present. Execute your script to generate the output files.