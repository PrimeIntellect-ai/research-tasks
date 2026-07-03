You are assisting a compliance officer auditing database access logs. The system currently uses a Python script (`/home/user/generate_report.py`) to query a SQLite database (`/home/user/audit.db`). However, the script is taking an extremely long time to run and is returning massively inflated severity scores. The compliance officer suspects the SQL query contains an implicit cross join and lacks proper window aggregation.

Your objectives:

1. **Extract Policy Parameters:** We lost the original text for the compliance policy, but a scan of the document is available at `/app/policy.png`. Read this image (you may need to install OCR tools like `tesseract-ocr` and `pytesseract`) to find the rolling window duration (in days) and the severity threshold.
2. **Fix the Query:** Rewrite the SQL query inside `/home/user/generate_report.py`. The query must:
   - Eliminate the implicit cross join.
   - Only consider "out-of-department" accesses (where the `resource_dept_id` in `access_logs` does not match the `dept_id` in `employees`).
   - Calculate the rolling sum of `severity` for these out-of-department accesses for each employee within the rolling time window specified in the policy image. (Hint: SQLite supports window functions like `SUM(...) OVER (...)`).
   - Filter the final results to only include employees whose maximum rolling severity sum strictly exceeds the threshold found in the policy image.
3. **Optimize:** The query must be performant. Create a script `/home/user/optimize.py` that connects to `/home/user/audit.db` and creates the necessary database indexes to optimize your new query. Run this script.
4. **Output Format:** The `generate_report.py` script must execute the query and dump the results to `/home/user/compliance_report.json` in the following exact format:
   ```json
   [
     {
       "emp_uid": "E-1042",
       "max_rolling_severity": 125
     },
     ...
   ]
   ```
   (Sort the output descending by `max_rolling_severity`, then ascending by `emp_uid`).

The automated test will verify the correctness of your output JSON. If correct, it will measure the execution time of your `generate_report.py` script. To pass, the script must execute in under 1.5 seconds.