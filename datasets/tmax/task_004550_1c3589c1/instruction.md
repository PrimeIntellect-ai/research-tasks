You are porting a legacy data processing tool to a minimal container environment. The tool, written entirely in Bash, validates and processes network request logs. However, due to missing dependencies and schema changes, it is currently broken. Your job is to perform a schema migration, resolve an ABI (Application Binary Interface) mismatch in its shared bash library, and implement a missing rate-limiting emulator.

All scripts must be written exclusively in Bash (using standard coreutils like `awk`, `sed`, `grep`, `mkdir`, etc.). Do not use Python, Perl, or other interpreters.

Here is what you need to do:

1. **Schema Migration**
There is a raw log file at `/home/user/data/raw.csv`. Its schema is `timestamp,ip,endpoint,user_agent`.
The processor now expects a new schema: `timestamp,ip,method,endpoint`.
Write a script `/home/user/app/migrate.sh` that reads `/home/user/data/raw.csv` and produces `/home/user/data/migrated_logs.csv`.
For every row, the `method` column must be set to the hardcoded string `GET`. The `user_agent` column must be dropped. 

2. **Shared Library ABI Wrapper**
The main processing script is located at `/home/user/app/processor.sh`. You are **not allowed to modify this file**.
It sources a library file at `/home/user/lib/libvalidate.sh`. 
`processor.sh` expects a function named `validate_ip_v2` to exist, but `/home/user/lib/libvalidate.sh` only provides the legacy `validate_ip` function. 
Modify `/home/user/lib/libvalidate.sh` to include a `validate_ip_v2` function that acts as a wrapper, simply calling the existing `validate_ip` function and passing its arguments transparently.

3. **Rate Limiting Emulator Implementation**
`processor.sh` delegates rate-limiting decisions to an external script at `/home/user/app/rate_limiter.sh`, which is currently missing.
Create `/home/user/app/rate_limiter.sh` and make it executable.
It will be called by `processor.sh` with two arguments: `$1` (IP address) and `$2` (Timestamp).
Your script must track request counts per IP per Timestamp (e.g., using a state directory or temporary file). 
- If an IP has strictly more than 2 requests for the **same** timestamp (i.e., this call represents the 3rd or greater request for that exact IP and exact second), the script must exit with status code `1` (rate limited).
- Otherwise, it must record the request and exit with status code `0` (allowed).

4. **Execution**
Once the above components are in place:
- Run `/home/user/app/migrate.sh`.
- Run `/home/user/app/processor.sh`.

If successful, `processor.sh` will produce `/home/user/output/final_processed.txt`.