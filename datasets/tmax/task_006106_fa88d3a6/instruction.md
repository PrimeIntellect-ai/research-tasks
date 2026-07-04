You are a developer debugging a failing build pipeline in your project directory at `/home/user/project`.

When you run the build script `/home/user/project/build.sh`, it fails during the data validation step. The pipeline consists of a Python script (`process_data.py`) that queries a local SQLite database (`data.db`), processes financial transaction records for a specific reporting period, and writes the results to `output.json`. A validation script (`validate.py`) then checks this output.

There are three distinct issues you must find and fix to make the build pass:
1. **Environment Misconfiguration:** The build script is failing to pass the correct reporting year to the Python script. The validator expects the report to be for the year `2023`, but the environment is either unconfigured or misconfigured, causing the script to fall back to the wrong year.
2. **Boundary Condition / Off-By-One Error:** The SQL query in `process_data.py` has a logic flaw in how it filters the `day` column. It is currently missing the first and last days of the month (days 1 and 31).
3. **Precision Loss Tracking:** The Python script aggregates floating-point amounts by sequentially adding them using standard `float` arithmetic. This introduces precision loss (e.g., resulting in values like `168.00000000000003`). You must modify `process_data.py` to calculate the exact sum without floating-point artifacts (e.g., using the `decimal` module or `math.fsum`) so that the final JSON outputs the exact, clean numerical value.

**Your goal:**
1. Identify and fix the environment variable issue in `/home/user/project/build.sh`.
2. Fix the SQL query boundary conditions in `/home/user/project/process_data.py`.
3. Fix the precision loss bug in the aggregation loop in `/home/user/project/process_data.py`.
4. Run `./build.sh` successfully.

Upon success, `./build.sh` will print "Build passed!" and `validate.py` will exit cleanly. The final verified state will be checked against the contents of `/home/user/project/output.json`.