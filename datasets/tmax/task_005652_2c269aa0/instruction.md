I am a compliance officer auditing our internal system access. We have a C++ extraction tool (`/home/user/extractor.cpp`) that queries an SQLite database (`/home/user/audit.db`) to find the latest 'DENIED' access attempts and exports them to a CSV file.

However, the report is generating completely wrong results. The SQL query hardcoded inside the C++ program has a logical error: it is missing a proper join condition between the tables, causing an implicit cross join. As a result, every denied access is being falsely attributed to every single employee in the database.

Your task is to:
1. Analyze the SQLite database schema in `/home/user/audit.db` to understand the relationships.
2. Fix the SQL query inside `/home/user/extractor.cpp` so that it correctly joins the relevant tables to associate the exact employee with their specific access log. 
3. Ensure the query filters for 'DENIED' status, sorts the results by the access timestamp in strictly descending order, and limits the output to exactly the 10 most recent denied events.
4. Compile the fixed program using `g++ /home/user/extractor.cpp -o /home/user/extractor -lsqlite3`.
5. Run the compiled program to generate the corrected `/home/user/audit_report.csv`.

The final `/home/user/audit_report.csv` should have the header `Name,Department,Resource,Timestamp` followed by the 10 correct rows. Do not change the CSV formatting logic in the C++ file, only fix the SQL query string.