You are a data scientist tasked with cleaning a multilingual product review dataset. The data is currently in a "wide" format, contains unnormalized Unicode text, and has some rows corrupted with invalid UTF-8 byte sequences.

Your goal is to write a Rust program that reads this dataset, cleans the text, reshapes it into a "long" format, and writes it back out to a CSV.

I have already created a basic Rust project skeleton for you at `/home/user/cleaner` with the `csv` and `unicode-normalization` crates in the `Cargo.toml`.

**Input Data:**
The input file is located at `/home/user/data/reviews.csv`. 
It has the following columns: `id`, `review_2023_01`, `review_2023_02`, `review_2023_03`.
Some of the text contains invalid UTF-8 bytes. Some of the valid UTF-8 text is in Unicode Normalization Form D (NFD).

**Your Rust program must perform the following operations:**
1. **Read the input CSV** (handling invalid UTF-8 by replacing invalid byte sequences with the Unicode Replacement Character `U+FFFD`).
2. **Reshape from Wide to Long:** Transform the data so that the output CSV has exactly three columns: `id`, `month`, and `review`. 
   - The `month` column should contain the suffix of the original column name (e.g., `2023_01`, `2023_02`, `2023_03`).
   - If a review cell is entirely empty (zero bytes), **do not** create a row for it in the long format.
3. **Normalize Unicode:** Convert all review text to Unicode Normalization Form C (NFC).
4. **Output:** Write the results to a standard CSV file at `/home/user/data/cleaned_reviews.csv` with a header row (`id,month,review`).

Compile and run your Rust program to generate the cleaned file.