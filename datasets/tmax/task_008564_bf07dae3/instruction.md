You are an data engineer troubleshooting an ETL pipeline. An upstream SQL query contained an implicit cross join bug, causing our event logs to explode with invalid records. It joined the `UserEvents` table with the `Departments` table without a proper join condition, resulting in every event being associated with every department in the company.

Your task is to write a Go program (`/home/user/pipeline.go`) that filters out the invalid records, sorts the valid ones, and extracts a specific paginated subset.

**Data Sources:**
1. `/home/user/data/valid_relationships.csv`: Contains the actual relationships between Users and Departments.
   Format: `UserID,DepartmentID`
2. `/home/user/data/corrupted_export.csv`: The bloated event log containing the cross-join garbage.
   Format: `EventID,UserID,DepartmentID,Timestamp,Action`

**Requirements for `/home/user/pipeline.go`:**
1. **Index Strategy & Graph Matching:** Read `/home/user/data/valid_relationships.csv` and build an efficient in-memory index (e.g., a map/hashset acting as a simple knowledge graph) to quickly verify if a `(UserID, DepartmentID)` edge is valid.
2. **Filtering:** Stream or read `/home/user/data/corrupted_export.csv`. Keep only the events where the `UserID` and `DepartmentID` pair exists in your valid relationships index.
3. **Sorting:** Sort the filtered (valid) events by `Timestamp` in **descending** order. If timestamps are identical, sort by `EventID` in **ascending** order (lexicographically).
4. **Pagination:** Implement pagination with a page size of `15`. We need you to extract exactly **Page 3** (which corresponds to items 31 through 45 in the sorted valid list, assuming 1-based indexing for pages).
5. **Output:** Write the results for Page 3 to `/home/user/page3.json` as a JSON array of objects. 

**Output Format for `/home/user/page3.json`:**
```json
[
  {
    "event_id": "E105",
    "user_id": "U22",
    "department_id": "D4",
    "timestamp": "2023-10-25T14:30:00Z",
    "action": "LOGIN"
  },
  ...
]
```

To complete the task:
1. Initialize a Go module in `/home/user` if necessary.
2. Write the Go code in `/home/user/pipeline.go`.
3. Run your Go program to generate `/home/user/page3.json`.