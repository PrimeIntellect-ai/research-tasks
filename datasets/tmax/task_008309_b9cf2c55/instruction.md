You are an AI assistant helping a compliance officer audit an internal system for segregation-of-duties violations. 

The company stores its audit logs in a document-oriented format, currently dumped into an SQLite database located at `/home/user/audit.db`. 
The database has a single table named `logs`, with a single column named `document` containing JSON strings. 

Your task is to:
1. Reverse engineer the schema of the JSON documents to identify system approval events. Note that the logs contain various types of events, and you only care about approvals.
2. Extract the requester and approver from each approval event to build an approval graph. An edge exists from User X to User Y if User Y approved a request made by User X.
3. Project this data into a graph and find all users who are part of a cyclic approval chain (e.g., User A's request is approved by User B, and User B's request is approved by User A, creating a cycle. Cycles can be of any length > 1).
4. Write a Python script `/home/user/find_cycles.py` that connects to the database, performs the extraction, detects the cycles, and writes the output.
5. The output must be saved to `/home/user/violators.json`.

Output format requirements for `/home/user/violators.json`:
- It must be a valid JSON file.
- It must contain a single JSON array of strings representing the names of all users involved in ANY cyclic approval chain.
- The list of names must be deduplicated and sorted alphabetically.

Example of expected output format:
```json
[
  "Alice",
  "Bob",
  "Charlie"
]
```