You are a data scientist working on an NLP project. You have been given a set of raw, uncleaned text records distributed across several JSON Lines (JSONL) files in `/home/user/raw_data/`. You need to build a data processing pipeline in Python that cleans, filters, and stratifies this dataset for model training.

Please write a Python script at `/home/user/clean_pipeline.py` and run it to produce the final dataset at `/home/user/cleaned_sampled.jsonl`. 

Your script must implement the following pipeline steps:

1. **Parallel Extraction**: Use Python's built-in `multiprocessing` or `concurrent.futures` modules to read and process the `.jsonl` files in `/home/user/raw_data/` in parallel. 
2. **Normalization & Tokenization**: For every record, extract the `text` field. 
   - Convert the text to lowercase.
   - Remove all characters EXCEPT alphanumeric characters (a-z, 0-9) and spaces.
   - Replace any multiple consecutive spaces with a single space, and strip leading/trailing spaces.
   - "Tokenize" the normalized text by splitting it by space.
3. **Filtering**: Discard any record that results in fewer than 3 tokens.
4. **Stratified Selection**: Group the remaining records by their `category` field. To ensure a deterministic and balanced dataset, select exactly 5 records for each category. If a category has fewer than 5 valid records, select all of them. To make the selection deterministic, sort the valid records in each category alphabetically by their `id` field, and pick the first 5.
5. **Loading**: Write the final selected records to `/home/user/cleaned_sampled.jsonl`. Each line must be a valid JSON object with exactly the following keys:
   - `id`: The original record ID.
   - `category`: The original category.
   - `normalized_text`: The string result from step 2.
   - `token_count`: An integer representing the number of tokens.

Ensure your script handles everything end-to-end. Once you have written the script, execute it so the final output file is generated.