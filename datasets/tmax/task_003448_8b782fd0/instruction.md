You are a log analyst tasked with investigating and cleaning up a messy data dump caused by an ETL job that failed and retried multiple times. The retry logic was flawed, leading to duplicate records. The records are multilingual user feedback messages.

The raw data is located in `/home/user/raw_data/` and consists of three files in different formats:
1. `data.csv`: Contains columns `user_id`, `timestamp`, `message`.
2. `data.jsonl`: JSON Lines format. Each line is an object with keys `uid`, `ts`, `msg`.
3. `data.xml`: An XML file with a root `<records>` element containing `<record>` elements. Each `<record>` has `<id>`, `<time>`, and `<text>` child elements.

Your goal is to build a Python pipeline that reads these files, standardizes the schema, computes a mathematical fingerprint for the messages to detect duplicates, deduplicates the records, and writes the clean data and statistics to specific output files.

### Step 1: Data Standardization and Fingerprinting
Read all records from the three files. Standardize the fields into `user_id` (integer), `timestamp` (integer), and `message` (string).
To detect duplicates despite encoding or minor formatting differences, compute a custom mathematical fingerprint for each `message`:
1. Normalize the `message` string using Unicode **NFKC** normalization.
2. Convert the normalized string to lowercase.
3. Compute the fingerprint using this formula:
   Let `primes` be the first 25 prime numbers: `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]`.
   For each character in the normalized, lowercased string at 0-based index `i`, calculate: `ord(char) * primes[i % 25]`.
   The `fingerprint` is the sum of these values modulo `1000000007`.

### Step 2: Deduplication
A record is considered a duplicate if another record exists with the **same `user_id`** and the **same `fingerprint`**.
When duplicates are found, keep only the record with the **earliest `timestamp`**. If timestamps are identical, keep the first one encountered (order of reading: CSV, then JSONL, then XML).

### Step 3: Output
1. Write the deduplicated records to a Parquet file at `/home/user/output/clean_data.parquet`. The Parquet file must have the following schema/columns: `user_id` (Int64), `timestamp` (Int64), `message` (String, keeping the original un-normalized text of the kept record), and `fingerprint` (Int64).
2. Write a statistics report to `/home/user/output/report.json` with the following structure:
```json
{
  "total_records_read": <int>,
  "total_duplicates_removed": <int>,
  "user_with_most_duplicates": <int>
}
```
*Note: `total_duplicates_removed` is the number of records discarded. `user_with_most_duplicates` is the `user_id` that had the highest number of discarded duplicate records.*

Make sure to create the `/home/user/output/` directory if it doesn't exist. You may install any necessary Python packages (like `pandas`, `pyarrow`, `lxml`) using `pip`.