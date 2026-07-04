You are a FinOps analyst tasked with automating the daily storage cost calculation for a cloud data archive. 

We have a legacy billing API wrapper located at `/home/user/billing_portal.sh`. Due to legacy security policies (similar to an SSH server that silently rejects key-based logins), this script strictly requires an interactive TTY session to accept its password. 

Your task consists of the following steps:
1. Use an `expect` script to interactively run `/home/user/billing_portal.sh`. When prompted for a password, provide `finops_secure`. Upon successful authentication, the script will print the current storage rate in the format `STORAGE_RATE_PER_MB=<value>`.
2. Measure the total disk space consumed by the directory `/home/user/data_archive` in Megabytes (where 1 MB = 1048576 bytes). Round up to the nearest whole integer.
3. Create a Rust project at `/home/user/cost_calc`. 
4. Write a Rust program in this project that reads two environment variables: `STORAGE_RATE_PER_MB` (retrieved from step 1) and `ARCHIVE_MB` (the integer calculated in step 2).
5. The Rust program must calculate the total cost (`ARCHIVE_MB` multiplied by `STORAGE_RATE_PER_MB`) and write the result to `/home/user/cost_report.txt` in exactly this format: `Total Cost: $<value>` (formatted to exactly two decimal places).
6. Execute your compiled Rust program with the correct environment variables so the final `cost_report.txt` file is generated.

Do not assume the archive size or the rate; you must extract them dynamically.