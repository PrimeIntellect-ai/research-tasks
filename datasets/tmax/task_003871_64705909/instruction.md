You are a compliance officer auditing an internal communications and financial transfer database for a financial firm.

The previous auditor left an SQLite database at `/home/user/compliance.db` and a SQL script at `/home/user/audit_report.sql`. 

Their script was supposed to calculate the total transfer amount sent by each employee, but **only** for employees who have sent at least one message containing the word "urgent" in the `messages` table. However, the script is currently producing incorrect, massively inflated totals because of an implicit cross join between the `transfers` and `messages` tables.

Your tasks are to fix the SQL report, reverse engineer the database model to perform network analysis, and summarize your findings.

1. **Fix the SQL Query**: Modify the logic in `/home/user/audit_report.sql` so that it accurately calculates the `total_sent` for employees who sent at least one message with the word "urgent", without duplicating transfer amounts. Save your corrected query to `/home/user/fixed_query.sql`. 
   - Note: The columns returned must be `name` and `total_sent`.

2. **Graph Analytics**: Reverse engineer the `compliance.db` schema to understand the relationship between employees and transfers. Treat the transfer data as a directed graph where an edge goes from `sender_id` to `receiver_id`. 
   - Find the employee who belongs to the `Trading` department and has the highest out-degree (the highest number of outgoing transfer transactions, ignoring the monetary amounts).

3. **Final Report**: Create a JSON file at `/home/user/audit_summary.json` containing exactly these two keys:
   - `"highest_transfer_employee"`: The string name of the employee who sent the highest total money (based on the output of your fixed query from step 1).
   - `"central_trader_id"`: The integer ID of the employee in the 'Trading' department with the highest out-degree centrality found in step 2.

Ensure your final JSON file is strictly valid and formatted correctly. You may use any tools or languages available to accomplish this.