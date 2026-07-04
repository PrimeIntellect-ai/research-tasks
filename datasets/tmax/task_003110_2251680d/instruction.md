You are a data analyst working with exported HR data. You have been given two CSV files representing a relational schema, and you need to project this data into a partitioned graph representation using a Bash script. 

The two files are located in `/home/user/`:
1. `employees.csv` - Contains employee details. 
   Schema: `emp_id,name,department_id`
2. `mentorships.csv` - Contains directed mentorship relationships (mentor to mentee). 
   Schema: `mentor_id,mentee_id`

Your task is to write a Bash script named `/home/user/process_graph.sh` that processes these CSVs and extracts intra-department mentorships. Specifically:
1. Identify all mentorship relationships where BOTH the mentor and the mentee belong to the EXACT SAME `department_id`.
2. Cross-reference the IDs to get the `name` of both the mentor and the mentee.
3. Materialize this filtered graph into a JSON file at `/home/user/same_dept_mentorships.json`.

The resulting JSON file must represent the edges grouped by `department_id`. 
The format must strictly be a JSON object where:
- Keys are the `department_id` (as strings).
- Values are lists of directed edges (lists of two strings: `[mentor_name, mentee_name]`).
- The edges within each department's list must be sorted alphabetically by the `mentor_name`, and if there's a tie, by the `mentee_name`.
- The output JSON must be correctly formatted/pretty-printed.

Example Output Format (`/home/user/same_dept_mentorships.json`):
```json
{
  "10": [
    [
      "Alice",
      "Bob"
    ],
    [
      "Bob",
      "Diana"
    ]
  ],
  "20": [
    [
      "Charlie",
      "Eve"
    ]
  ]
}
```

Constraints:
- Your script must be written in Bash (`/home/user/process_graph.sh`) and should be executable (`chmod +x`).
- You may use standard Unix tools (e.g., `awk`, `join`, `sort`, `jq`, `sed`, `grep`) within your bash script. You may also use `python3` or `sqlite3` inside the script if you wish, but invoking it via a single shell script is required.
- Run your script so that the output file `/home/user/same_dept_mentorships.json` is generated before you complete the task.