I am organizing a new textual dataset for my research and need to run a quick tokenization benchmark to set up my experiment tracking. 

Please do the following on my Linux terminal:
1. Create a Python virtual environment named `venv` in `/home/user/`.
2. Activate the virtual environment and install the `tiktoken` package.
3. I have a dataset file at `/home/user/dataset.jsonl` containing JSON objects with `id` and `text` fields.
4. Write and execute a Python script that reads this file, tokenizes the `text` field of each line using the `cl100k_base` encoding from `tiktoken`, and counts the number of tokens.
5. Identify the top 5 records with the highest token counts.
6. Write these top 5 records to a CSV file at `/home/user/longest_tokens.csv`. The CSV must have exactly two columns: `id` and `token_count` (include a header row). Sort the output by `token_count` in descending order. If there is a tie in token count, sort by `id` in alphabetical ascending order.

Ensure all file paths are exact and the output CSV is formatted perfectly.