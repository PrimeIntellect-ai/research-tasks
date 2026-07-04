You are assisting a compliance officer auditing an organization's IT systems. The organization has strict data access policies, one of which is: **No employee with the role of "Contractor" should have access (direct or indirect) to the "sys_finance" system.**

Currently, the organization's data is fragmented:
1. HR data is stored in a CSV file at `/home/user/hr_data.csv`. It contains columns: `emp_id`, `name`, `role`, `manager_id`.
2. IT access data is stored in a Knowledge Graph represented as a JSONL (JSON Lines) file at `/home/user/access_graph.jsonl`. Each line is an object representing a directed edge: `{"source": "...", "relation": "...", "target": "..."}`.
   - Relations can be `"MEMBER_OF"` (e.g., a user is a member of a group, or a group is a member of another group).
   - Relations can be `"HAS_ACCESS"` (e.g., a group has access to a system).

Your task is to build a Rust application that maps these two data representations and performs a hierarchical graph query to identify all compliance violations.

**Requirements:**
1. Create a new Rust project in `/home/user/compliance_auditor`.
2. The Rust program must read both `/home/user/hr_data.csv` and `/home/user/access_graph.jsonl`.
3. It must find all employees who:
   - Have the `role` equal to `"Contractor"`.
   - Have a valid path in the access graph starting from their `emp_id` and ending at `"sys_finance"`.
   - A valid path consists of zero or more `"MEMBER_OF"` relations followed by exactly one `"HAS_ACCESS"` relation. (e.g., `emp_id` -> `"MEMBER_OF"` -> `GroupA` -> `"MEMBER_OF"` -> `GroupB` -> `"HAS_ACCESS"` -> `"sys_finance"`).
4. The program must export the findings to `/home/user/violations.json`.
5. The output must be a tightly formatted JSON array of objects, sorted alphabetically by `emp_id`. Each object must have the exact following structure:
   ```json
   [
     {
       "emp_id": "E...",
       "name": "...",
       "path": ["E...", "GroupA", "GroupB", "sys_finance"]
     }
   ]
   ```
   *Note: The `path` array must list the sequence of nodes from the employee ID to "sys_finance".*

**Execution:**
Once you have written the code, compile it using `cargo build --release` and run it so that the `/home/user/violations.json` file is generated.