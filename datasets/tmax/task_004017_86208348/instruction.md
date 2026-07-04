You are an AI assistant helping a medical researcher organize and analyze a set of disorganized datasets. 

I have a SQLite database located at `/home/user/research_data.db`. It contains several tables related to an ongoing clinical study, but the previous research assistant didn't document the schema well. 

Your task is to write a Go program that analyzes this database, extracts a specific aggregated dataset, validates it, and saves it to a JSON file.

Here is what you need to do:
1. **Schema Analysis:** Inspect the SQLite database `/home/user/research_data.db` to understand the relationships between the patients, their assigned clinical trials, and the observation outcomes. You will need to figure out the exact table and column names yourself.
2. **Go Program Creation:** Write a Go program at `/home/user/organize_data.go`. Initialize any necessary Go modules in `/home/user/`. You can use standard libraries and the `github.com/mattn/go-sqlite3` driver.
3. **Parameterized Querying & Chaining:** Your program must accept two command-line flags: `--min-age` (integer) and `--condition` (string). It should execute a parameterized SQL query that joins the relevant tables to fetch records for patients matching the given minimum age (inclusive) and exact condition. Calculate the average recovery days for each distinct treatment arm among these filtered patients.
4. **Validation:** Process the aggregated results through a validation pipeline in your Go code. A valid output record must meet these criteria:
   - `treatment_arm` must be exactly one of: `"Arm A"`, `"Arm B"`, or `"Placebo"`. Any other values (e.g., `"UNKNOWN"`, `NULL`, `"Arm C"`) are invalid data anomalies and must be excluded.
   - `avg_recovery_days` must be a valid float greater than or equal to 0.0.
5. **Output Generation:** Write the validated aggregated records as a single JSON array to `/home/user/summary_results.json`. The JSON array should contain objects with exactly two keys: `"treatment_arm"` (string) and `"avg_recovery_days"` (float rounded to 2 decimal places). Sort the JSON array alphabetically by `"treatment_arm"`.

Finally, after compiling/writing your program, execute it once with the arguments: `--min-age 30 --condition "Asthma"`. Ensure the final `/home/user/summary_results.json` is generated.