You are a data analyst tasked with building a reproducible text processing pipeline in Bash to clean and tokenize a dataset of reviews. 

You have been provided with a raw dataset at `/home/user/raw_data.csv`. The file has the following columns: `item_id`, `publish_date`, `raw_text`.

Your goal is to write a bash script at `/home/user/pipeline.sh` that automates the environment setup, enforces data schema rules, and performs text tokenization.

The script `/home/user/pipeline.sh` must perform the following actions when executed:
1. Create a Python virtual environment in `/home/user/venv`.
2. Activate the virtual environment and install the `csvkit` package via `pip`.
3. Process `/home/user/raw_data.csv` to enforce the following schema rules (rows violating these rules must be completely dropped):
    * `item_id` must be purely numeric (integers only).
    * `publish_date` must strictly follow the `YYYY-MM-DD` format.
4. Tokenize the `raw_text` column for the valid rows with the following steps:
    * Convert all text to lowercase.
    * Remove all characters *except* lowercase letters (`a-z`) and spaces. (Numbers and punctuation should be removed).
    * Collapse any sequence of multiple spaces into a single space.
    * Strip any leading or trailing spaces.
5. Output the cleaned and tokenized data to a new valid CSV file at `/home/user/clean_tokens.csv` with the headers: `item_id,publish_date,tokens`.
6. Write the final count of valid data rows (excluding the header) to `/home/user/row_count.txt` as a single integer.

Ensure your pipeline script is reproducible and properly handles CSV quoting (commas inside the `raw_text` fields). You may use inline Python within your Bash script to safely parse the CSV if you prefer, but the entire pipeline must be contained and executed via `/home/user/pipeline.sh`.

Once you have created the script, run it to generate the final outputs.