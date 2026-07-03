You are a Data Engineer building an ETL pipeline to prepare a text corpus for an NLP model. 

Your task is to write and execute a Python script that processes a raw dataset located at `/home/user/raw_data.csv` and outputs a cleaned, tokenized dataset to `/home/user/processed_dataset.jsonl`.

The input CSV has the following columns: `doc_id`, `text`, `author`, `views`.

You must implement the following ETL rules exactly:
1. **Missing Value Handling:**
   - Drop any rows where the `text` column is empty, whitespace-only, or missing (NaN/Null).
   - If the `author` column is missing, fill it with the string `"Unknown"`.
   - If the `views` column is missing, fill it with the median of all valid (non-missing) `views` in the dataset. (Calculate the median before removing any outliers in the next step. If the median is a float, round it down to the nearest integer).

2. **Outlier Removal:**
   - Remove any rows where `views` is strictly greater than 100,000 (assumed to be bot traffic).

3. **Text Cleaning and Tokenization:**
   - Convert the `text` to lowercase.
   - Replace any non-alphanumeric character (anything that is not a-z or 0-9) with a single space.
   - Split the resulting string by whitespace to create a list of tokens. (Ignore empty strings).
   - Count the number of tokens.
   - **Text Outlier Removal:** After tokenization, drop any rows where the `token_count` is less than 5 or greater than 50.

4. **Output Generation:**
   - Save the final processed data as a JSONL (JSON Lines) file at `/home/user/processed_dataset.jsonl`.
   - Each line must be a valid JSON object with the following keys:
     - `doc_id`: The original document ID (integer or string as read, but preferred string).
     - `cleaned_text`: The lowercase, alphanumeric-only text (tokens joined by a single space).
     - `tokens`: The list of extracted token strings.
     - `token_count`: The integer number of tokens.
     - `author`: The author name.
     - `views`: The views (integer).

You may use `pandas` or standard Python libraries. Please write the script, run it, and ensure the output file is generated correctly.