You are a compliance analyst tasked with generating an automated security audit trail for an internal Python web application. The application's source code and configuration files are located in `/home/user/audit_target`.

Your objective is to review the application, identify specific security flaws, and generate a structured audit trail report. 

Perform the following tasks:
1. **Service Auditing**: Inspect the application code (`/home/user/audit_target/app.py`) to determine the exact TCP port the web application is configured to bind and listen to.
2. **File Permission Control**: Analyze the files in `/home/user/audit_target/`. Identify any file that is world-writable (accessible by 'others' with write permissions).
3. **Vulnerability Analysis**: 
   - Identify the exact line number in `app.py` where a SQL Injection (SQLi) vulnerability is introduced (specifically, the line where a raw, unparameterized SQL query is executed using user input).
   - Identify the exact line number in `app.py` where a Cross-Site Scripting (XSS) vulnerability exists (specifically, the line where unsanitized user input is directly returned in an HTTP response).

Once you have gathered this information, generate the final audit trail by creating a JSON file at `/home/user/audit_report.json` with the following exact structure:

```json
{
  "service_port": <integer port number>,
  "world_writable_files": ["<absolute path to file 1>", "<absolute path to file 2>"],
  "sqli_line_number": <integer line number>,
  "xss_line_number": <integer line number>
}
```

Constraints:
- The `world_writable_files` array must contain the absolute paths of all world-writable files inside the `/home/user/audit_target` directory, sorted alphabetically. If there is only one, it should still be in the array.
- Line numbers must be integers matching the exact line in `app.py` where the vulnerable function (e.g., `execute` for SQLi, or the `return` statement for XSS) is called.
- Ensure the JSON is strictly valid.