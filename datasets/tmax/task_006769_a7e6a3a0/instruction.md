You are a data scientist responsible for cleaning and aggregating multilingual customer feedback datasets. You have been given two datasets containing product reviews from different regions, in different formats, and with varying data quality.

Your goal is to validate the records, normalize and tokenize the multilingual text, filter out stop words, and extract the top 5 most frequent words for each product category.

**Input Files:**
1. `/home/user/data/reviews_na.csv`: A CSV file containing North American reviews. Columns: `id, user_id, product_category, rating, timestamp, feedback`.
2. `/home/user/data/reviews_eu.jsonl`: A JSON Lines file containing European reviews. Each line is a JSON object with keys: `id, user_id, product_category, rating, timestamp, feedback`.
3. `/home/user/data/stopwords.txt`: A plain text file containing one stop word per line (UTF-8 encoded).

**Phase 1: Constraint-Based Data Validation**
You must combine the records from both files and filter out any invalid rows. A record is VALID only if ALL the following hold true:
*   `user_id`: Must be exactly 8 to 12 characters long and contain ONLY alphanumeric characters (A-Z, a-z, 0-9).
*   `rating`: Must be an integer between 1 and 5 (inclusive).
*   `timestamp`: Must strictly match the format `YYYY-MM-DDTHH:MM:SSZ`.

**Phase 2: Text Normalization & Tokenization**
For all valid records, process the `feedback` text as follows:
1.  Convert the entire text to lowercase.
2.  Remove all characters that are NOT Unicode letters or whitespace. (e.g., remove numbers, punctuation, emojis). Note: Accented characters like `é`, `ü`, `ñ` ARE Unicode letters and must be kept. You can replace non-letters with a space.
3.  Tokenize the text into individual words by splitting on whitespace.
4.  Remove any words that appear in the `stopwords.txt` file (case-insensitive). Also, drop any empty string tokens.

**Phase 3: Aggregation & Sorting**
Group the cleaned tokens by `product_category`.
For each category, determine the top 5 most frequent words.
If there is a tie in frequencies, break the tie by sorting the words alphabetically (a-z). If a category has fewer than 5 unique words, include all of them in sorted frequency order.

**Output:**
Write the final aggregated results to `/home/user/output/top_terms.json`.
The file must be a valid JSON dictionary where the keys are the `product_category` strings, and the values are lists of strings representing the top words for that category.

Example format:
```json
{
  "Electronics": ["battery", "screen", "good", "quality", "fast"],
  "Clothing": ["shirt", "cotton", "blue", "fit", "soft"]
}
```

Ensure the output directory `/home/user/output` exists before writing. Write a Python script to perform this entire pipeline and execute it in the terminal.