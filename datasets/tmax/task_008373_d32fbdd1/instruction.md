As a data scientist, you need to clean and combine a multilingual dataset of product reviews collected from two different upstream sources. The datasets contain noisy text, inconsistent encodings, and duplicate submissions.

You have two files in your home directory:
1. `/home/user/reviews_part1.csv` (Columns: `review_id`, `product_id`, `text`, `timestamp`)
2. `/home/user/reviews_part2.json` (Array of objects with keys: `review_id`, `product_id`, `text`, `timestamp`)

Write a Python script to process the data and generate a final summary report at `/home/user/cleaned_product_stats.csv`.

Your pipeline must perform the following steps:
1. **Union**: Read both datasets and combine them into a single tabular structure.
2. **Unicode & Text Normalization**: For the `text` column:
   - Apply Unicode NFKC normalization.
   - Convert all text to lowercase.
   - Remove all characters *except* alphanumeric characters (letters and numbers from any language/script) and spaces. Punctuation and emojis should be removed. (Hint: Regular expression `[^\w\s]` is useful, but ensure unicode word characters are matched).
   - Replace any sequences of multiple spaces with a single space, and strip leading/trailing spaces.
3. **Deduplication**: There are duplicate reviews based on the *normalized text*. If multiple rows have the exact same normalized text, keep ONLY the row with the earliest `timestamp` (using standard string comparison for the ISO8601 timestamps). Drop the others.
4. **Feature Extraction**: Calculate a `word_count` for each surviving review. A "word" is defined as any sequence of characters separated by a single space in the normalized text. (If the normalized text is empty, word count is 0).
5. **Aggregation**: Group the cleaned, deduplicated dataset by `product_id`. For each product, calculate:
   - `review_count`: The total number of unique reviews.
   - `avg_word_count`: The average `word_count` of those reviews, rounded to exactly 2 decimal places.
6. **Sorting and Output**: Sort the final aggregated data first by `review_count` in descending order, and then by `product_id` in ascending order (alphabetically).

Save the result to `/home/user/cleaned_product_stats.csv`. The output CSV must have exactly these headers: `product_id,review_count,avg_word_count`.

Do not hardcode the expected outputs; your script should dynamically process the data.