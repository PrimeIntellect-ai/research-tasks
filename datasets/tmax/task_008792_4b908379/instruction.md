You are an AI assistant helping a data scientist clean and merge a messy dataset. We have two JSON-lines files located in `/home/user/`:
1. `/home/user/users.jsonl`
2. `/home/user/transactions.jsonl`

However, the pipeline is broken because `users.jsonl` contains malformed unicode escape sequences. Standard JSON parsers break when encountering them (e.g., `\u00ZZ` or `\u12` instead of 4 valid hex digits).

Your task is to write a Python script (or multiple scripts) that orchestrates a multi-stage data processing pipeline to do the following:

**Phase 1: Data Cleaning & Parsing**
* Read `/home/user/users.jsonl`.
* Detect and handle invalid unicode escape sequences. An invalid sequence is defined as the literal string `\u` followed by exactly 4 characters where at least one character is NOT a valid hexadecimal digit (0-9, a-f, A-F). 
* Replace the `\u` and those 4 invalid characters entirely with the string `[?]`.
* Successfully parse the cleaned JSON lines.

**Phase 2: Data Masking**
* For each parsed user record, anonymize the `email` field by replacing its entire value with the string `***@***.***`.

**Phase 3: Parallel Processing & Joins**
* Read `/home/user/transactions.jsonl`.
* Join the transaction records with the cleaned, masked user records based on `user_id` (from transactions) matching `id` (from users).
* Using Python's `multiprocessing` module (to ensure parallel data processing), calculate the Euclidean distance between the user's `home_coords` `[x1, y1]` and the transaction's `tx_coords` `[x2, y2]`. 
* The distance formula is: `sqrt((x2 - x1)^2 + (y2 - y1)^2)`.
* Add a new boolean field `"flagged"` to the merged record. Set it to `true` if the distance is strictly greater than `10.0`, otherwise `false`.

**Phase 4: Output**
* Save the fully joined, masked, and flagged records to `/home/user/final_output.jsonl`.
* The output file must be a valid JSON-lines file.
* Each line must contain all fields from the transaction record, plus the `name`, `email` (masked), and `home_coords` from the user record, and the new `flagged` field.
* Sort the final output file ascending by `tx_id` (e.g., `t1`, `t2`, `t3`).

Make sure your final script runs without requiring root privileges. You may create intermediate files if needed.