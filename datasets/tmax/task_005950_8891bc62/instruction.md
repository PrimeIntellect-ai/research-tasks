You are a database administrator tasked with optimizing and implementing a graph-like query using a NoSQL database. A company stores its employee hierarchy in a MongoDB database, and you need to build a Go tool that retrieves a paginated, sorted list of all indirect and direct subordinates for a given manager.

Here is your task:

1. **Environment Setup**:
   - Download the official MongoDB 6.0+ or 7.0+ Linux binaries (tarball) and extract it to `/home/user/mongodb`.
   - Start a local MongoDB instance in the background on port `27017`. Use `/home/user/mongo_data` for the dbpath and `/home/user/mongo.log` for the logpath.
   - You have been provided an initial dataset at `/home/user/employees.json` (you will need to wait for the setup script to create this or create a sample to test with, but assume it exists with fields `_id`, `name`, and `managerId`).
   - Import the `/home/user/employees.json` into a database named `company` and a collection named `employees`.

2. **Go Program Implementation**:
   - Create a Go module in `/home/user/app`.
   - Write a Go program at `/home/user/app/query.go`.
   - The program should use the official MongoDB Go driver.
   - In the program, ensure that an ascending index exists on the `managerId` field to optimize the graph traversal.
   - Implement an aggregation pipeline that:
     a) Starts with a specific manager's `_id` (parameterized).
     b) Uses a graph traversal operator (like `$graphLookup`) to find all direct and indirect subordinates (where a subordinate's `managerId` points to their manager's `_id`).
     c) Flattens the result so each subordinate is its own document.
     d) Filters out the original manager (only return the subordinates).
     e) Sorts the subordinates by their `_id` in ascending order.
     f) Applies pagination (skip and limit).
   - The Go program should accept three command-line arguments: `manager_id` (string), `skip` (int), and `limit` (int). Example: `go run query.go "E1" 0 5`
   - The program must execute the pipeline and write the exact resulting JSON array of subordinate documents to `/home/user/output.json`. The output must be valid JSON, indented with 2 spaces.

3. **Execution**:
   - Run your program to find the subordinates of manager `"E2"`, skipping the first `1` result, and limiting to `3` results.
   - Ensure the final output file is at `/home/user/output.json`.

*Note: You do not have root access. All installations and executions must occur within user-space.*