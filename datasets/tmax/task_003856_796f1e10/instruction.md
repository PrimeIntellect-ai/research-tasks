You are helping debug a failing data processing build in a CI/CD pipeline. The workspace is located at `/home/user/build_workspace`. 

The build pipeline usually runs a script that reads 50 JSON data files concurrently, extracts a `"value"` integer from each, stores the records in a SQLite database (`results.db`), and deletes the JSON files as they are successfully processed to save space. 

However, the build has been failing intermittently with a crash, leaving the workspace in an incomplete state. Currently:
1. The `results.db` database is left behind, possibly with uncommitted transactions in its Write-Ahead Log (WAL) or journal, representing the successfully processed and deleted JSON files.
2. The remaining unprocessed JSON files are left in `/home/user/build_workspace/data/`. One of these files causes the processing script to crash due to an unexpected encoding or serialization issue.

Your task is to:
1. Recover all the successfully processed values from the SQLite database (make sure to account for any data still in the WAL).
2. Identify the remaining unprocessed JSON file(s) in the `data/` directory, diagnose the encoding/serialization issue, and properly read its `"value"`.
3. Calculate the grand total sum of all `"value"` fields (those recovered from the database + those from the remaining JSON files).
4. Write this single integer sum to a new file at `/home/user/final_metric.txt`.

Ensure your final output file contains ONLY the integer sum. You may write any Python scripts you need to accomplish this.