We have an ETL pipeline that ingests customer reviews from various regional databases. Recently, a failure in the pipeline caused several jobs to retry, producing duplicate records. Furthermore, due to different encoding standards across our regional databases, some duplicates have different Unicode normalization forms (e.g., NFC vs. NFD). Additionally, minor text corruption during transit introduced small typos in some duplicated payloads.

We need to clean this data by identifying and deduplicating these records. 

You have been provided with a directory of raw batch files in JSON format at `/home/user/data/raw_reviews/`. 
Each JSON file contains a list of dictionaries with the following keys:
- `record_id` (string)
- `user_id` (string)
- `timestamp` (integer - Unix epoch)
- `review_text` (string - multi-language text)

Your task is to write a Python script (and execute it) to process these JSON files and produce a single, deduplicated CSV file at `/home/user/data/clean_reviews.csv`.

**Deduplication Rules:**
1. Group the records by `user_id`.
2. Within each `user_id` group, compare the `review_text` of the records to find duplicates.
3. **Similarity Condition:** First, normalize all `review_text` to Unicode NFC form. Two records (within the same `user_id` group) are considered duplicates if the Levenshtein distance between their normalized `review_text` strings is **less than or equal to 2**.
4. **Resolution:** When duplicates are found, keep the record with the oldest (minimum) `timestamp`. Discard the newer duplicates. If timestamps are identical, keep the one with the lexicographically smaller `record_id`.
5. Records that do not share a `user_id` are never considered duplicates of each other.
6. A group of duplicates might contain more than two records. (Assume the duplicate relation is transitive for this dataset, i.e., all duplicates of a single original record will cluster together).

**Output Requirements:**
- Format: CSV (comma-separated), with a header row.
- Columns required: `record_id`, `user_id`, `timestamp`, `review_text`.
- The `review_text` in the output must be the NFC-normalized version.
- Sort the final CSV rows by `record_id` in ascending alphabetical order.
- Save the result to `/home/user/data/clean_reviews.csv`.

You may install external libraries (like `Levenshtein` or `editdistance`) using `pip` if needed.