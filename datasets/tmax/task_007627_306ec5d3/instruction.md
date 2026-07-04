You are a database administrator tasked with optimizing and consolidating query results from our multi-model database system. We have recently extracted data from three different storage engines (Relational, Document, and Graph), and we need a high-performance C++ tool to aggregate this data, map the relationships, and output a validated JSON summary.

Your task is to write a C++ program located at `/home/user/aggregator.cpp` that reads the following three files from `/home/user/data/`:

1. **`users.csv` (Relational Export)**
   Format: `user_id,name,department`
   Example: `U1,Alice,Engineering`

2. **`permissions.json` (Document Export)**
   Format: JSON array of objects.
   Example: `[{"uid": "U1", "roles": ["admin", "deploy"]}, {"uid": "U2", "roles": ["read"]}]`

3. **`reports_to.txt` (Graph Export - Adjacency List)**
   Format: `manager_id:report_id1,report_id2,...`
   Example: `U1:U2,U3`

**Requirements for the C++ program:**
- It must accept three arguments (paths to the three files) and write the output to `/home/user/output.json`.
- For every manager listed in `reports_to.txt`, it must aggregate their team's data. A team consists of the manager and their direct reports.
- Extract the manager's `department` from `users.csv`.
- Calculate the `team_size` (1 manager + number of direct reports).
- Aggregate and deduplicate all `roles` from `permissions.json` for everyone in the team (manager + reports). The roles must be sorted alphabetically.
- Output a strict JSON array of objects to `/home/user/output.json` sorted by `manager_id` (alphabetically).
- You can use the popular single-header JSON library provided at `/home/user/include/json.hpp`.

**Output Schema Validation:**
Your output must exactly match this JSON schema (indentation 2 spaces):
```json
[
  {
    "manager_id": "U1",
    "department": "Engineering",
    "team_size": 3,
    "combined_roles": [
      "admin",
      "deploy",
      "read"
    ]
  }
]
```

**Steps to complete:**
1. Write the C++ code to `/home/user/aggregator.cpp`.
2. Compile it using `g++ -std=c++11 -I/home/user/include /home/user/aggregator.cpp -o /home/user/aggregator`.
3. Run the program to generate `/home/user/output.json`: `./aggregator /home/user/data/users.csv /home/user/data/permissions.json /home/user/data/reports_to.txt`