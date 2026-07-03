You are an AI assistant helping a data scientist clean a messy, multi-lingual dataset of social media posts.

The dataset is located at `/home/user/raw_data.jsonl`. It is a JSON Lines file where each line is a JSON object with the following keys: `id` (string), `lang` (string), and `text` (string). The file simulates a very large dataset, so your solution should process it line-by-line rather than loading all texts into memory at once (though keeping a few top candidates in memory per language is fine).

You need to write a script (Python is recommended) that performs the following data cleaning and stratification pipeline:

1. **Text Normalization**: For each record, normalize the `text` field using Unicode NFKC normalization, then convert the string to lowercase. 
2. **Filtering**: Discard any record where the normalized text is strictly less than 15 characters long.
3. **Deduplication**: Remove duplicate records based on the *normalized* text. If multiple records have the exact same normalized text, keep only the one with the lexicographically smallest `id`.
4. **Stratified Selection**: For each language (`lang`), select exactly the 3 records with the longest normalized text (measured by character count). 
   - *Tie-breaking*: If two records have the same length, prioritize the one with the lexicographically smallest `id`.
5. **Output**: Write the selected records to `/home/user/stratified_longest.jsonl`.
   - The output must be in JSON Lines format.
   - Each line must be a JSON object containing `id`, `lang`, and `text` (this must be the **normalized** text).
   - The file must be sorted first by `lang` (alphabetically, ascending), then by text length (descending), and finally by `id` (alphabetically, ascending).

Ensure your script is efficient and strictly follows the normalization and sorting rules. Once your script is ready, run it to generate the final output file.