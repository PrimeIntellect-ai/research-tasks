You are an automation specialist investigating a bug in an ETL (Extract, Transform, Load) pipeline. A recent network failure caused a retry job to trigger, but due to an encoding glitch in the messaging queue, some of the retried records became slightly mutated and bypassed the exact-match deduplication filter. 

Your task is to identify these mutated duplicates.

1. **Transfer and Extract:** 
   The raw exports are located in a simulated remote drop directory at `/tmp/remote_drop/etl_exports.tar.gz`. Copy this archive into your local workspace at `/home/user/etl_workspace/` and extract it. Inside, you will find two files: `run1.csv` (the initial load) and `run2_retry.csv` (the retry load).

2. **Feature Extraction:**
   Each CSV file has the format `transaction_id,receipt_id,status`. You only need to analyze the `receipt_id` (the second column). All `receipt_id` strings are exactly 12 characters long.

3. **Distance & Similarity Computation:**
   We define a "mutated duplicate" as a `receipt_id` in `run2_retry.csv` that has a **Hamming distance of exactly 1** compared to any `receipt_id` in `run1.csv`. (A Hamming distance of 1 means the strings are identical except for exactly one character at the same position).

4. **Reporting:**
   Create a file at `/home/user/etl_workspace/mutated_duplicates.csv` that lists these near-matches. The file should contain one pair per line, separated by a comma, in the format:
   `receipt_id_from_run1,receipt_id_from_run2`

Ensure you only output pairs with a Hamming distance of exactly 1 (exclude exact matches or pairs with a distance of 2 or more). You must accomplish this using standard Bash utilities (like `awk`, `grep`, `cut`, etc.) without writing external scripts in languages like Python or Perl.