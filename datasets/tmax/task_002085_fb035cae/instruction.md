You are a data analyst troubleshooting a data pipeline. A recent system crash corrupted our primary database indices, leaving us with raw, exported CSV dumps that contain duplicate, stale rows for many records. 

Your objective is to build a Bash-based data processing pipeline that reconstructs the correct current state of our company's operations (data model reverse engineering) and identifies a specific structural anomaly (knowledge graph pattern matching).

The raw data is located in `/home/user/data/` and consists of three CSV files:
1. `employees.csv` (Columns: `emp_id,name,dept_id,version`)
2. `projects.csv` (Columns: `proj_id,proj_name,dept_id,version`)
3. `works_on.csv` (Columns: `emp_id,proj_id,version`)

Because of the export glitch, an entity (e.g., an employee or project) might appear multiple times with the same ID. The `version` column is an integer; you must *only* consider the row with the highest `version` number for any given ID to be the active record.

**Your Task:**
Create an executable Bash script at `/home/user/find_anomalies.sh` that performs the following:
1. Deduplicates the CSV data to retain only the latest versions of each entity.
2. Cross-references the datasets (query-to-pipeline chaining) to find all instances of a specific anomalous graph pattern: **An employee working on a project that belongs to a different department than the employee's own department.**
3. Outputs the results as a strictly formatted JSON array to `/home/user/anomalies.json`.

The final `/home/user/anomalies.json` file must be an array of objects containing exactly the employee's name and the project's name, sorted alphabetically by the employee's name.

Example output format:
```json
[
  {
    "emp_name": "Alice",
    "proj_name": "Project Apollo"
  },
  {
    "emp_name": "Bob",
    "proj_name": "Project Zeus"
  }
]
```

Requirements:
- You must use Bash utilities (like `awk`, `jq`, `join`, `sort`, etc.) for your pipeline.
- Make sure to give your script execute permissions (`chmod +x /home/user/find_anomalies.sh`).
- Execute your script so that `/home/user/anomalies.json` is generated.