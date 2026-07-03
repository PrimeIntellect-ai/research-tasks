You are a data scientist preparing a dataset for a machine learning model. The raw data extraction process failed to format the logs correctly, leaving you with a messy log file at `/home/user/raw_users.log`. 

Your task is to parse, clean, validate, extract features from this log file, and output a clean CSV file using ONLY standard bash command-line tools (like `awk`, `sed`, `grep`, `sort`, `tr`, etc.). Do not write Python or Perl scripts; stick strictly to Bash and coreutils.

Here are the requirements for the data pipeline:

1. **Extraction**: Extract the `user_id`, `email`, `age`, and `joined` date from each line. The lines have inconsistent prefixes, but the data is generally separated by ` | ` and labeled with `User: `, `email: `, `age: `, and `joined: `.
2. **Validation**: 
   - Drop any row where the `age` is not a strictly positive integer (contains non-digits).
   - Drop any row where the `email` is invalid (for this task, an email is valid strictly if it contains exactly one `@` symbol).
3. **Cleaning / Normalization**: Convert all `email` addresses to strictly lowercase.
4. **Feature Extraction**:
   - Create a new feature `email_domain` which is everything after the `@` in the email.
   - Create a new feature `joined_year` which is the 4-digit year extracted from the `joined` date (assumed format YYYY-MM-DD).
5. **Deduplication**: Deduplicate the final records based on `user_id`. If there are multiple valid records for the same `user_id`, keep only one (any one is fine, as long as the user_id is unique in the final output).
6. **Formatting**: Save the output to `/home/user/clean_features.csv`.
   - The file must contain a header row exactly as follows: `user_id,email_lower,email_domain,age,joined_year`
   - The records must be sorted numerically by `user_id`.
   - The delimiter must be a comma (`,`).

Example input line:
`[INFO] 2023-10-10 User: 101 | email: ALice@Example.com | age: 25 | joined: 2023-05-12`

Expected processed record for the above:
`101,alice@example.com,example.com,25,2023`