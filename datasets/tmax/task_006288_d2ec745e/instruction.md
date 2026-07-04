You are a data engineer tasked with building an ETL pipeline to process ad impression logs. You need to read raw data, enforce a strict schema, engineer new features, apply a Bayesian smoothing technique to calculate a probability score, and output the processed data.

You can use any programming language of your choice.

**Input Data:**
A raw JSON Lines file located at `/home/user/raw_data.jsonl`.
Each line is a JSON object representing an ad event.

**Requirements:**

1. **Schema Enforcement:**
   Read `/home/user/raw_data.jsonl` and strictly validate each record. A valid record MUST meet ALL the following criteria:
   - `user_id`: must be an integer.
   - `ad_id`: must be an integer.
   - `clicks`: must be an integer, and `clicks >= 0`.
   - `impressions`: must be an integer, and `impressions > 0`.
   - Logical constraint: `clicks` cannot be greater than `impressions`.
   - `timestamp`: must be a string in ISO 8601 format (e.g., `"2023-10-15T08:30:00Z"`).
   
   If a record is missing any of these fields, has extra fields, or violates ANY of the type or logical constraints, it is considered INVALID.
   - Write all INVALID raw JSON records (exactly as they appeared in the input) to `/home/user/invalid_records.jsonl`.
   - Process all VALID records through the remaining steps.

2. **Feature Engineering:**
   For each valid record, extract the hour of the day from the `timestamp` field (0-23) based on UTC. Store this as a new feature called `hour_of_day`.

3. **Bayesian Inference (Probability Modeling):**
   Calculate a smoothed Click-Through Rate (CTR) using a Beta-Binomial conjugate model.
   Assume a global prior distribution for CTR with parameters $\alpha = 2$ and $\beta = 100$.
   For each record, calculate the posterior mean of the CTR using the formula:
   `bayesian_ctr = (clicks + alpha) / (impressions + alpha + beta)`
   Round `bayesian_ctr` to exactly 4 decimal places.

4. **Output Generation:**
   Save the processed valid records to `/home/user/processed_data.csv`.
   The CSV must have the following exact header row:
   `user_id,ad_id,hour_of_day,clicks,impressions,bayesian_ctr`
   The rows must be sorted in ascending order first by `user_id`, and then by `ad_id`.

**Execution:**
You must write the code, run it, and ensure the output files are correctly generated in `/home/user/`.