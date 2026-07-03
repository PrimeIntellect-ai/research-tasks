You are an IT compliance officer auditing an internal document system. The previous auditor left a daily reporting script that has a critical flaw: when aggregating NoSQL-style document data, it effectively performs an implicit cross-join between user roles and user access events, massively inflating the access counts for users with multiple roles.

Your task is to analyze the data schema, perform a cross-query summarization, and write a correct aggregation script to replace the broken one. 

**Data Source:**
You are provided with a JSONL dataset at `/home/user/data/users.jsonl`. 
Each line is a JSON object representing a user, containing:
- `user_id` (string)
- `department` (string)
- `roles` (array of strings)
- `access_logs` (array of objects, each containing `doc_id` and `timestamp`)

**The Bug:**
The previous script calculated the number of accesses by unwinding the `roles` array and then unwinding the `access_logs` array. For a user with 3 roles and 4 access logs, this created 12 records, inflating the department's total access count. 

**Your Objective:**
Write a script in Python, Node.js, or bash (your choice) that correctly processes `/home/user/data/users.jsonl` to compute the actual compliance metrics. 

You must generate a final report at `/home/user/compliance_report.json` with the following strict JSON schema (an array of objects, sorted alphabetically by `department`):

```json
[
  {
    "department": "Engineering",
    "total_accesses": 42,
    "unique_roles": ["admin", "developer", "viewer"]
  },
  ...
]
```

**Requirements:**
1. `total_accesses` must be the true total number of access events for all users in that department (no Cartesian explosion).
2. `unique_roles` must be a deduplicated, alphabetically sorted list of all roles held by users in that department.
3. The root of the JSON file must be an array, sorted alphabetically by the `department` string.
4. Output your final validated JSON exactly to `/home/user/compliance_report.json`.

You have complete freedom in how you write the aggregation logic, as long as the final schema and values are mathematically correct and properly handle the nested arrays.