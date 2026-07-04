You are acting as an automated compliance officer auditing our internal network. We have experienced a potential security incident where unauthorized personnel may have accessed a restricted system (Node `F`) by hopping through the internal network.

Your goal is to write a pure Bash script (using only standard CLI tools like `awk`, `sed`, `grep`, `jq`, and shell built-ins) that analyzes the system logs, employee directory, and network topology, and outputs a strictly formatted JSON report of all compliance violations.

You will find the following data files in `/home/user/data/`:
1. **`employees.csv`**: A CSV file containing `user_id,name,role`. The first line is the header.
2. **`access_logs.json`**: A JSON file containing an array of access records. Each record has `log_id`, `user_id`, `entry_node`, `target_node`, and `timestamp`.
3. **`network.txt`**: A text file representing the undirected network topology. Each line contains two node names separated by a space, representing a direct network connection (edge) between those two systems.

**Compliance Rules & Tasks:**
1. **Identify Violations:** System Node `F` is highly restricted. Only users with the `Admin` role in `employees.csv` are permitted to have `F` as their `target_node`. Any access to `F` by a non-Admin is a compliance violation.
2. **Path Tracing:** For every violation identified, you must calculate the shortest network path length (number of edges) from the user's `entry_node` to the restricted `target_node` (`F`) using the topology in `network.txt`.
3. **Data Aggregation & Cross-mapping:** For each violation, extract the user's name from the CSV, the entry node from the JSON log, and your computed shortest path length.
4. **Generate Report:** Output the results to `/home/user/violations.json`. The output must be a valid JSON array of objects, sorted alphabetically by `user_id`. Each object must exactly match this schema:
   ```json
   [
     {
       "user_id": "<string>",
       "name": "<string>",
       "entry_node": "<string>",
       "target_node": "<string>",
       "path_length": <integer>
     }
   ]
   ```

Write your script to perform this analysis automatically and save it as `/home/user/audit.sh`. Execute the script to generate `/home/user/violations.json`.

Constraints:
- You must use Bash and standard utilities (e.g., `awk`, `jq`). Do not use Python, Perl, or Node.js.
- Ensure the JSON output is strictly formatted and valid.