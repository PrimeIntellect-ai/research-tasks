You are a data engineer tasked with building an ETL pipeline that loads graph data and exposes an aggregation API.

We have a custom, in-memory graph processing engine vendored at `/app/vendored/graph-etl-engine`. However, our previous engineer left it in a broken state. When concurrent transactions run during the ETL load phase, the engine frequently deadlocks. 

Your tasks are:
1. **Fix the Vendored Package:** Inspect `/app/vendored/graph-etl-engine/transaction.go`. There is a synchronization bug causing deadlocks when inserting edges concurrently (hint: think about lock acquisition order). Fix the source code directly in the vendored package.
2. **Reverse Engineer Data Model:** We have a raw N-Triples data dump at `/home/user/data/dump.nt`. Reverse engineer the schema to understand the relationships between Employees, Salaries, and Departments.
3. **Build the ETL Server:** Create a new Go project at `/home/user/etl-server`. Initialize a Go module and use a `replace` directive to point `graph-etl-engine` to the local vendored path.
4. **Implement Data Loading:** Write logic to parse `/home/user/data/dump.nt` and load it into the engine using concurrent transactions (e.g., loading different entity types in parallel goroutines to prove the deadlock is fixed).
5. **Expose an HTTP API:** Start an HTTP server listening on `127.0.0.1:8080`.
   - All requests must require the header: `Authorization: Bearer SecureGraphETL2024`. Reject others with 401 Unauthorized.
   - Implement `GET /summary?dept=<DepartmentName>`. Using the graph engine, perform a cross-query aggregation to find:
     - The department manager's name (the person who `MANAGES` the department).
     - The total number of employees working in the department (including the manager, if they work there).
     - The sum of salaries for all employees in that department.
   - The response should be JSON in this exact format:
     `{"department": "Engineering", "manager": "Alice", "employee_count": 3, "total_salary": 250000}`

Run your server in the background once compiled. Ensure it starts successfully and listens on the correct port.