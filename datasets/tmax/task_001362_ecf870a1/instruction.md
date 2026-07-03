You are a database administrator tasked with prototyping a highly optimized aggregation pipeline engine in C. We are migrating some heavy analytics workloads from our NoSQL database into a custom C extension for performance. 

You need to write a C program that simulates a NoSQL aggregation pipeline over a set of exported document collections (JSON lines format).

Here is the setup:
There are two collections exported as JSONL files:
1. `/home/user/users.jsonl` - Contains user documents. Schema: `{"user_id": "string", "name": "string", "region": "string"}`
2. `/home/user/orders.jsonl` - Contains order documents. Schema: `{"order_id": "string", "user_id": "string", "total": integer, "status": "string"}`

Your C program (which you should write to `/home/user/aggregate.c`) must implement the following logical NoSQL pipeline:
1. **Filter ($match)**: Read `/home/user/orders.jsonl` and keep only orders where `status` is exactly `"completed"` AND `total` is strictly greater than `100`.
2. **Join ($lookup)**: Map the filtered orders to the users in `/home/user/users.jsonl` using the `user_id` field.
3. **Group ($group)**: Calculate the `total_spent` for each `user_id` (summing the `total` of their filtered orders). Note: Include the user's `region` in this grouped result.
4. **Sort ($sort)**: Sort the resulting grouped records descending by `total_spent`. If there is a tie, sort ascending by `user_id` alphabetically.
5. **Paginate ($skip / $limit)**: Skip the first 1 record, and limit the output to the next 3 records.

**Output:**
Your C program must write the final paginated results to `/home/user/results.csv`.
The CSV must have the following exact header and format:
```csv
user_id,region,total_spent
UXX,RegionName,XXX
```

**Environment & Tools:**
- You may use standard Unix utilities to create the initial environment.
- For parsing JSON in C, you can install and use the `cJSON` library (e.g., via `sudo apt-get install libcjson-dev`). If you use `cJSON`, remember to link it during compilation (e.g., `-lcjson`).
- Assume you have `gcc` installed. Compile your program and execute it to generate the CSV.

Do not use external scripts (like Python or jq) to do the actual data processing; the core pipeline logic must be implemented in your C program.