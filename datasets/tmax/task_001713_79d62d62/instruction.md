I need you to act as a Data Scientist and clean up a dataset. We had an ETL job fail and retry multiple times, resulting in a text file (`/home/user/raw_etl_dump.txt`) with many duplicate, unnormalized records. 

Please write a Rust program to process this data. Initialize a new Cargo project at `/home/user/etl_cleaner`.

Your Rust program must perform the following operations in a single streaming pass (do not load the entire file into memory at once):

1. **Stream Reading**: Read `/home/user/raw_etl_dump.txt` line by line.
2. **Standardization & Normalization**: For each line:
   - Convert the entire string to lowercase.
   - Trim leading and trailing whitespace.
   - Replace any sequences of multiple spaces with a single space.
   - Discard the line if it becomes empty.
3. **Deduplication**: Keep track of the normalized strings you have seen. If a normalized string has already been processed, skip it entirely.
4. **Tokenization & Rolling Statistics**: For each *new, unique* normalized record:
   - Count the number of words (tokens separated by a single space).
   - Maintain a sliding window of the word counts for the last **3** unique records processed (if less than 3 records have been processed, use however many are currently available).
   - Calculate the rolling average of these word counts.
5. **JSONL Output**: Append the results to `/home/user/processed_dataset.jsonl` as JSON Lines. Each line must be a valid JSON object with the following keys:
   - `"text"`: The normalized string.
   - `"words"`: The integer word count of the string.
   - `"rolling_avg"`: The rolling average word count as a float, rounded to exactly two decimal places (e.g., `3.50`, `3.67`).

Write and run the Rust program to generate the final `processed_dataset.jsonl` file. Do not use external crates other than `serde` and `serde_json` (if needed) to minimize compilation time.