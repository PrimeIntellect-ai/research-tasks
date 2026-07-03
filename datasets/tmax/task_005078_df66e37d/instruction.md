You are acting as an AI assistant to a compliance officer. We need to audit our internal communication network to identify employees in the "Investment" department who are acting as information sinks (receiving the most messages). 

I have extracted three files from our system databases, located in `/home/user/audit_data/`:
1. `/home/user/audit_data/users.csv` - Contains employee information.
2. `/home/user/audit_data/departments.csv` - Contains department mappings.
3. `/home/user/audit_data/comms.log` - A headerless comma-separated log file of internal messages.

The `comms.log` file is an undocumented extract. By inspecting the data, you must reverse engineer its schema to determine which columns represent the sender ID and receiver ID (hint: the first column is a UNIX timestamp, the second is the sender's user ID, and the third is the receiver's user ID).

Your task is to write a Rust program that accomplishes the following:
1. Parse the three files to reconstruct the relational data model.
2. Project this data into a directed graph where nodes are employees and edges represent a message sent from one employee to another.
3. Compute the **In-Degree Centrality** for each employee (the total count of incoming messages they received).
4. Filter the results to include *only* employees belonging to the "Investment" department.
5. Sort the filtered employees by their In-Degree in descending order. If there is a tie, sort by their user ID in ascending order.
6. Retrieve the top 2 employees from this sorted list (pagination/limiting).
7. Write the final output to `/home/user/flagged_employees.json` as a JSON array of objects with the following exact structure:
   ```json
   [
     {
       "uid": 123,
       "name": "EmployeeName",
       "in_degree": 42
     }
   ]
   ```

Requirements:
- Create your Rust project in `/home/user/audit_tool/`.
- You can use external crates (like `csv`, `serde`, `serde_json`, or `petgraph` if you wish, though you can also compute it natively).
- Do not use root privileges. 
- Ensure your program compiles via `cargo build --release` and runs successfully, generating the required JSON file.