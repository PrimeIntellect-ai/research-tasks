I need you to help me clean and merge some messy user review datasets from different regional databases. I'm building a multi-stage data processing pipeline in Python.

I have three files located in `/home/user/raw_data/`:
1. `users.parquet` (UTF-8 encoding): Contains user metadata with columns `user_id` (integer), `username` (string), and `signup_date` (string).
2. `reviews_asia.csv` (Shift-JIS encoding): A CSV file with headers containing `user_id` and `review_text`.
3. `reviews_eu.json` (UTF-16 encoding): A JSON file containing a list of objects with keys `id` (matches user_id) and `comment` (the review text).

Your task is to write a Python script that orchestrates the following pipeline:
1. **Load and Decode:** Read all three datasets using their respective correct character encodings.
2. **Merge Data:** Union the reviews from the Asia and EU datasets, then perform an inner join with the `users` dataset based on the user ID. 
3. **Tokenization and Normalization:** For the combined review text:
   - Convert all text to lowercase.
   - Remove all characters EXCEPT lowercase English letters (a-z), numbers (0-9), and whitespace.
   - Tokenize the text by whitespace and rejoin it with a single space (i.e., remove extraneous multiple spaces or tabs).
4. **Export:** Save the final processed data to `/home/user/cleaned_reviews.jsonl`. 

The output file MUST be in JSON Lines format (one JSON object per line) and sorted alphabetically by `username`. 
Each JSON line must have exactly these three keys:
- `username` (from users data)
- `signup_date` (from users data)
- `normalized_review` (the cleaned review text)

Please write and execute the Python script to generate the `/home/user/cleaned_reviews.jsonl` file.