You are a data analyst working with a legacy system. We have an old, undocumented, compiled tool located at `/app/legacy_parser`. This tool takes a CSV file containing an organization's knowledge graph (employee reporting hierarchy and performance scores) and exports it into a highly specific JSON format. We need to decommission this binary and replace it with a verifiable Python script.

Your task is to write a Python script at `/home/user/process_data.py` that behaves EXACTLY like `/app/legacy_parser`. 

The legacy tool is invoked exactly like this:
`/app/legacy_parser <input.csv>`
And it writes the result to standard output. 

Your script will be invoked exactly like this:
`python3 /home/user/process_data.py <input.csv>`
It must also write the exact same output to standard output.

**Input CSV Schema:**
The input CSV has no header. The columns are:
1. `employee_id` (integer)
2. `manager_id` (integer or empty string for the CEO/root)
3. `department` (string)
4. `performance_score` (float)

**Expected Processing:**
By experimenting with the legacy binary, you will notice it performs a hierarchical calculation. For each employee, it identifies their entire management chain (recursive hierarchy). It then calculates a specific analytical metric: the average `performance_score` of all employees in the same `department` who are at the exact same "depth" in the hierarchy (window function/analytical aggregation). 

**Expected Output Schema (JSON):**
A JSON array of objects, sorted by `employee_id` ascending. Each object must have:
- `"emp_id"`: integer
- `"chain_length"`: integer (number of managers above them; root is 0)
- `"dept_peer_avg"`: float (average performance score of all employees in the same department with the same `chain_length`, rounded to 2 decimal places)

Reverse engineer the exact behavior of `/app/legacy_parser` (you can run it, pass it dummy CSVs, and inspect the output) and write the Python script to replicate it. Ensure your script gracefully handles standard edge cases (e.g., disconnected subgraphs or missing manager IDs).