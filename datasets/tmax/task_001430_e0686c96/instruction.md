You are a data analyst tasked with processing international survey feedback. We have received survey data from three different regions, but the data collection systems used different character encodings and outputted the data in a wide format. 

Your task is to build a Python data pipeline to clean, reshape, deduplicate, and summarize this data.

**Input Data:**
Three CSV files are located in `/home/user/input_data/`:
1. `survey_na.csv` (Encoded in UTF-8)
2. `survey_eu.csv` (Encoded in ISO-8859-1)
3. `survey_ap.csv` (Encoded in Shift_JIS)

Each file has the following columns: `user_id`, `timestamp`, `q1_feedback`, `q2_feedback`, `q3_feedback`.

**Processing Requirements:**
1. **Encoding Handling:** Read all three CSV files correctly using their respective encodings to prevent text corruption, and combine them into a single dataset.
2. **Wide-to-Long Reshaping:** Convert the dataset from wide format to long format. The resulting columns should be `user_id`, `timestamp`, `question`, and `feedback`. The `question` column should contain the values 'q1', 'q2', or 'q3' (derived from the original column names: `q1_feedback`, `q2_feedback`, `q3_feedback`). Drop any rows where the `feedback` is entirely empty or only whitespace.
3. **Hash-based Deduplication:** Unfortunately, a bug in the survey system caused identical feedback strings to be submitted by bot accounts. You must remove exact duplicate feedback texts.
   - First, strip leading and trailing whitespace from the `feedback` text.
   - Compute the SHA-256 hash of the stripped text (encoded as UTF-8).
   - If multiple rows have the exact same feedback hash across the *entire* combined dataset, keep **only** the row with the earliest `timestamp` (chronological order). If timestamps are identical, keep the one with the lexicographically smaller `user_id`. 
   - Add a new column called `feedback_hash` containing the hex digest of the SHA-256 hash.
4. **Sorting:** Sort the final deduplicated dataset by `question` (ascending), then `timestamp` (ascending), then `user_id` (ascending).

**Outputs:**
You must create a directory `/home/user/processed/` and save two files:

1. `/home/user/processed/clean_data.csv`: The final, sorted, long-format data. It must be encoded in UTF-8 and contain exactly these columns in this order: `user_id`, `timestamp`, `question`, `feedback_hash`, `feedback`.
2. `/home/user/processed/summary.json`: A JSON file containing the count of unique, surviving feedback entries per question. The format must be exactly:
```json
{
  "q1": <count>,
  "q2": <count>,
  "q3": <count>
}
```

Ensure your script is self-contained and handles the data purely through Python (you may install pandas or other libraries via pip if needed).