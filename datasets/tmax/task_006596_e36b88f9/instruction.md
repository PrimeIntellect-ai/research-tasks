You are tasked with writing a C program to process configuration change logs for a fleet of servers. The system tracks raw configuration strings and server metadata, but the data needs to be cleaned, joined, anonymized, and analyzed before it can be used for compliance tracking.

You have two input files located in your home directory (`/home/user/`):
1. `config_log.txt`: A chronological pipe-separated (`|`) file of configuration changes. Format: `timestamp|server_id|raw_config_string`
2. `metadata.txt`: A pipe-separated (`|`) file of server ownership metadata. Format: `server_id|owner_email`

Write a C program at `/home/user/process_configs.c`, compile it to `/home/user/process_configs`, and run it to produce an output file at `/home/user/processed_logs.csv`.

The output file `/home/user/processed_logs.csv` must be a comma-separated values (CSV) file with the following columns in order, representing each row from `config_log.txt`:
`timestamp,server_id,masked_email,cleaned_config,cumulative_changes`

Your C program must implement the following data processing rules:
1. **Join**: Merge each log entry with its corresponding `owner_email` from `metadata.txt` using `server_id`. If a `server_id` is not found in `metadata.txt`, default the email to `unknown@unknown.com` before applying the masking rule.
2. **Masking (Anonymization)**: Anonymize the `owner_email` by replacing all characters before the `@` symbol with a single asterisk `*`, EXCEPT the very first character. For example, `admin-web@company.com` becomes `a*@company.com`. `unknown@unknown.com` becomes `u*@unknown.com`.
3. **Cleaning (Normalization)**: The `raw_config_string` must be cleaned by removing ALL non-alphanumeric characters (including spaces, punctuation, etc.) and converting all alphabetic characters to lowercase. For example, ` Nginx= V1.1 ` becomes `nginxv11`.
4. **Rolling Statistic**: Calculate the `cumulative_changes` for the specific `server_id`. This is an integer representing the number of times this specific `server_id` has appeared in the `config_log.txt` up to and including the current record.

Example Output Row:
`1620000000,S1,a*@company.com,nginxv11,1`

Requirements:
- Read the files efficiently. You can assume there are no more than 100 metadata records and 1000 log records, and lines do not exceed 256 characters.
- Your code must be written purely in C. Standard POSIX libraries are allowed.
- Ensure the output file exactly matches the specified format without any trailing spaces or extra characters.