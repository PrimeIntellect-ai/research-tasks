As a data scientist, you need to clean and sample a dataset of messy customer support chats to prepare for a downstream machine learning task.

You are provided with a raw CSV file at `/home/user/raw_chats.csv`. It contains two columns: `interaction_id` and `raw_text`.

Write a Python script to process this data according to the following rules:

1. **Information Extraction**:
   - Extract the "issue category" from `raw_text`. The category is always the single word immediately following the exact string `"Issue: "`. 
   - Normalize this category string by converting it to lowercase and stripping any surrounding whitespace or punctuation (e.g., `"Billing."` becomes `"billing"`, `" shipping "` becomes `"shipping"`).
   - If a row does not contain the substring `"Issue: "`, drop the row entirely.

2. **Feature Extraction**:
   - Create a boolean feature called `has_email` which is `True` if `raw_text` contains a valid email address, and `False` otherwise. Use a basic regex (e.g., `\S+@\S+\.\S+`) to detect emails.

3. **Stratification & Deterministic Sampling**:
   - From the cleaned data, take a stratified sample: select exactly 2 rows for each unique category.
   - To ensure deterministic results, sort the valid rows within each category by `interaction_id` in ascending lexicographical order, and select the first 2 rows. If a category has fewer than 2 rows, include all of them.

4. **Output formatting**:
   - Save the sampled data to `/home/user/processed_samples.csv`.
   - The output CSV must have exactly these columns: `interaction_id`, `category`, `has_email`.
   - The rows in the output CSV must be sorted primarily by `category` (ascending, alphabetical), and secondarily by `interaction_id` (ascending).

5. **Pipeline Logging**:
   - Append a summary log to `/home/user/process.log` with exactly this format:
     `Pipeline finished. Processed {total_input} rows. Saved {total_output} rows across {num_categories} categories.`
   - Note: `{total_input}` refers to the total number of rows in the original CSV (excluding the header).

You may use `pandas` or standard Python libraries. Write and execute the script in your terminal to generate the required files.