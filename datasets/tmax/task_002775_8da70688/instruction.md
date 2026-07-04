As a data analyst, you have been tasked with auditing several organizational hierarchy datasets stored as CSV files. Your goal is to build a robust validation pipeline that checks these files for structural integrity, validates their implicit schemas, and detects circular reporting chains (e.g., employee A reports to B, who reports to C, who reports back to A). 

To accomplish this, you must write a script named `/home/user/hierarchy_validator.py`. Your script will process these CSVs by loading them into an SQLite database and running recursive queries.

**Constraints & Requirements:**

1. **Vendored Dependency:** You must use the `sqlite-utils` package provided in `/app/sqlite-utils-3.35` to load the CSVs and build the indexes. *Note: We have observed that this specific local build has a bug causing corrupted indexes and stale rows when creating non-unique indexes. You will need to debug and fix this package before your pipeline can work correctly.*
2. **Schema Reverse Engineering:** The CSVs do not have standardized column names. Your script must dynamically identify which column represents the `employee_id` (usually the first column or contains 'id'), which represents the `parent_id` (contains 'parent' or 'manager'), and validate that the output schema conforms to this structure.
3. **Recursive Detection:** Once loaded and indexed, your script must use an SQLite Recursive CTE to find any circular reporting loops.
4. **Execution and Output:** 
   Your script must take a single file path as an argument:
   `python3 /home/user/hierarchy_validator.py <path_to_csv>`
   - If the file is a valid hierarchy (no cycles, valid schema), the script MUST print exactly: `CLEAN: <filename>` and exit with code 0.
   - If the file has a circular dependency or invalid schema, the script MUST print exactly: `EVIL: <filename>` and exit with code 1.

You will find a corpus of CSVs to test against in `/home/user/data/clean/` (which your script must accept) and `/home/user/data/evil/` (which your script must reject).

Write the script, fix the vendored package, and ensure your validator successfully categorizes the entire dataset.