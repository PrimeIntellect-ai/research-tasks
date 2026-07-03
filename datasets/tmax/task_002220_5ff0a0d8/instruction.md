You are acting as a compliance officer auditing an internal system for unauthorized data access. We have three isolated systems that track employee data, active sessions, and access logs, but our automated reporting system has failed due to database corruption.

Your task is to write a C++ program that manually correlates data across these three systems to generate a compliance report.

**System Details:**
1. **MongoDB (Hierarchy Data)**: Running on `127.0.0.1:27017`. Database: `corporate`, Collection: `employees`.
   Documents look like: `{ "emp_id": "E100", "manager_id": "E001" }`. 
   The CEO is `E001`. The hierarchy is a tree (employees can manage other employees).
2. **Redis (Risk Data)**: Running on `127.0.0.1:6379`.
   Keys are formatted as `risk:{emp_id}` (e.g., `risk:E100`), containing a string representing a risk multiplier (e.g., `"1.5"` or `"2.0"`).
3. **SQLite (Access Logs)**: Located at `/home/user/access_logs.db`.
   Table: `logs (log_id TEXT, emp_id TEXT, timestamp INTEGER, action TEXT)`.
   *Crucial Note*: The primary index on the `emp_id` column in SQLite was corrupted during a recent storage fault. Standard queries like `SELECT * FROM logs WHERE emp_id = 'E100'` will return stale or incomplete results because the B-Tree is broken. You must find a way to query the table while bypassing the corrupted index (e.g., forcing a full table scan).

**Your Objective:**
Write and compile a C++ program at `/home/user/auditor.cpp` (compiled to `/home/user/auditor`) that:
1. Connects to MongoDB to recursively find all indirect and direct subordinates of the manager with `emp_id` `"E042"` (an executive under investigation).
2. Retrieves all access logs from the SQLite database for these specific subordinates where the `action` is `"EXPORT"`. You must ensure you do not miss any records due to the corrupted index.
3. Cross-references the `emp_id` with Redis to retrieve their risk multiplier. If no risk multiplier exists in Redis, assume `"1.0"`.
4. Outputs the findings to `/home/user/compliance_report.csv` with the exact header: `log_id,emp_id,risk_multiplier`.

**Constraints & Notes:**
- You must write the solution in C++. You may use `libmongocxx`, `hiredis`, and `sqlite3` C/C++ libraries.
- The output CSV must be strictly formatted without spaces after commas.
- Your output will be graded by an automated system that checks the F1 score of the discovered `log_id`s compared to the ground truth.