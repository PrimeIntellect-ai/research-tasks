You are acting as a systems engineer assisting a compliance officer. We are auditing our internal financial and access systems. 

The previous compliance reporting system was written in C, and it contained a severe bug: when generating employee audit summaries, it performed an implicit cross-join between the `transactions` and `access_logs` tables, exponentially inflating both the total transaction amounts and the number of system accesses reported.

We have disabled the old system, but we preserved a patched, stripped binary at `/app/audit_oracle`. This binary takes a single integer argument (`employee_id`) and safely prints the *correct* aggregated totals for that employee to standard output. However, we cannot use this binary in production because it lacks network capabilities and cannot be integrated into our modern dashboard.

Your task is to build a new Python-based microservice that correctly queries the database and serves these compliance summaries over HTTP.

**Requirements:**

1. **Analyze the Database:**
   A SQLite database is located at `/home/user/audit.db`. Inspect its schema and understand the relationships between the `employees`, `transactions`, and `access_logs` tables. 

2. **Understand the Correct Aggregation:**
   You can use the `/app/audit_oracle <employee_id>` binary to see the correct `total_tx_amount` and `total_access_count` for any employee. Your new SQL queries must return these exact numbers, completely avoiding the cross-join trap that plagued the old system.

3. **Build the API Service:**
   Create a Python HTTP web service (using Flask, FastAPI, or standard library) that listens on `127.0.0.1:8080`.
   
   The service must expose a single `GET` endpoint:
   `/api/audit/summary`
   
   It must accept a query parameter `emp_id`.
   
   It must require an Authorization header:
   `Authorization: Bearer ComplianceAudit2024`
   (Return a 401 Unauthorized status if missing or incorrect).
   
   If successful, it must return a JSON response in this exact format:
   ```json
   {
     "emp_id": 1,
     "total_tx_amount": 150.50,
     "total_access_count": 5
   }
   ```
   *Note: If an employee has no transactions or access logs, the respective totals should be `0` or `0.0`.*

4. **Security Constraint:**
   The `emp_id` parameter must be handled securely using parameterized SQL queries. The compliance verifier will attempt basic SQL injection (e.g., `emp_id=1 OR 1=1`) to ensure your implementation is robust. If the injection succeeds or causes a 500 server error instead of safely returning no results/404/400, the audit fails.

Please write the service, start it in the background, and ensure it is listening on port 8080.