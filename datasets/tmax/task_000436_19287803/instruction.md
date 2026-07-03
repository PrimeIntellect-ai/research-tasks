You are acting as a technical assistant to a compliance officer auditing an organization's legacy infrastructure. 

We have an SQLite database at `/app/audit.db` containing access logs and employee hierarchy data. The schema contains three tables: `Employees`, `Resources`, and `AccessLogs`. The database is currently unindexed and query performance for compliance checks is abysmal. 

Furthermore, our legacy system generated a cryptographic signature (`hash_sig`) for each access log. The proprietary tool that generated these signatures is provided as a stripped binary at `/app/verify_sig`. 

Your task is to build a high-performance compliance auditing API in **C** that identifies tampered access logs.

**Requirements:**

1. **Database Optimization (Index Strategy):**
   Analyze the schema in `/app/audit.db` and execute SQL commands to create necessary indexes. Your indexes must optimize for recursive hierarchy queries (finding all subordinates of a manager) and sorting by timestamps.

2. **Compliance Verification Algorithm:**
   Analyze or reverse-engineer the `/app/verify_sig` binary. It takes three integer arguments (`emp_id`, `res_id`, `timestamp`) and prints an integer signature to stdout. To ensure high performance in your server, you should ideally reverse-engineer its internal logic and implement the signature generation directly in your C code, rather than calling the binary via `fork`/`exec` for every row.

3. **API Server (multi_protocol):**
   Write a C program that starts an HTTP web server listening on `127.0.0.1:8080`. 
   - You may use raw sockets or install a library like `libmicrohttpd-dev`.
   - The server must handle `GET /tampered?manager_id=<id>&page=<p>&limit=<l>`
   
4. **Query & Filtering Logic (Graph Pattern & Pagination):**
   When the endpoint is called:
   - Perform a recursive CTE query to find all employees who report directly or indirectly to `manager_id` (including the manager themselves).
   - Retrieve all `AccessLogs` for these employees.
   - Recompute the signature for each log using the logic from `verify_sig`. A log is "tampered" if the `hash_sig` in the database does NOT match the computed signature.
   - Sort the tampered logs by `timestamp` strictly descending. If timestamps are equal, sort by `log_id` ascending.
   - Apply pagination based on the `page` (1-indexed) and `limit` query parameters.

5. **Response Format:**
   Return a valid JSON response with `HTTP/1.1 200 OK` and `Content-Type: application/json`.
   Format:
   ```json
   {
     "manager_id": 1,
     "page": 1,
     "limit": 2,
     "tampered_logs": [
       {"log_id": 45, "emp_id": 3, "res_id": 9, "timestamp": 1600000000, "db_sig": 12345, "expected_sig": 54321},
       {"log_id": 52, "emp_id": 8, "res_id": 2, "timestamp": 1599999000, "db_sig": 11111, "expected_sig": 22222}
     ]
   }
   ```
   If there are no tampered logs or the page is out of bounds, return an empty array for `tampered_logs`.

Place your C source code at `/home/user/audit_server.c`, compile it, and run the server in the background so it is actively listening on port 8080 when you complete your response.