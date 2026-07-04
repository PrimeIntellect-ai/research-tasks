You are an IT support technician. We have received an urgent ticket (Ticket #8843) regarding our legacy data export tool. The tool is supposed to read a list of user IDs, query our SQLite database to resolve user aliases and fetch user details, and then output a JSON report. 

However, the automated nightly job is currently hanging indefinitely.

The system setup is as follows:
- The main script is located at: `/home/user/export_tool.py`
- The input list of IDs is at: `/home/user/input_ids.txt`
- The SQLite database is at: `/home/user/records.db`
- A wrapper script used to run the job is at: `/home/user/run_export.sh`

Your task is to:
1. Diagnose why the script is hanging (you may use system call tracing or simply analyze the code and run it).
2. Fix the corrupted input handling: the script currently gets stuck if it encounters malformed, non-numeric data in `input_ids.txt`. Modify `/home/user/export_tool.py` so that it completely skips any lines that cannot be parsed as an integer, instead of getting stuck in an infinite loop.
3. Fix the query result debugging/loop issue: the database contains a circular alias reference (e.g., ID A points to ID B, which points back to ID A). Modify the `resolve_alias` function in `/home/user/export_tool.py` to detect cycles. If a circular alias chain is detected, abort resolving the alias and simply return the *original* `user_id` that was passed to the function.
4. Run `/home/user/run_export.sh` successfully so that it generates the final output at `/home/user/export_results.json`.
5. Create a summary file at `/home/user/ticket_resolution.txt` with exactly two lines containing your findings:
   - Line 1: `Corrupted input: <the exact corrupted string found in the input file>`
   - Line 2: `Circular alias IDs: <comma-separated list of the IDs involved in the cycle, e.g., 5,6>`

Ensure your final JSON output and the text file are placed exactly at the specified paths.