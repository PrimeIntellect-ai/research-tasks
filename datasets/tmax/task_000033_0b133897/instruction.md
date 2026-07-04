You are assisting a compliance officer who is auditing an organization's internal access systems. We have an undocumented SQLite database located at `/home/user/compliance.db`. 

Your task is to write a Bash script at `/home/user/generate_audit.sh` that identifies security compliance violations for a specific management chain. 

Requirements for the script:
1. It must accept exactly one argument: a target Employee ID.
2. It must inspect the structure of `/home/user/compliance.db` to understand the schema (you will need to reverse-engineer the table and column names related to employees, systems, and access logs).
3. It must use a recursive SQL query (CTE) to find the target employee and **all** of their direct and indirect subordinates.
4. For this entire group of employees (the target and all subordinates), it must find all access events where the employee accessed a system that requires a higher clearance level than the employee currently holds.
5. The script must securely pass the Employee ID to the SQLite command as a parameter (do not just concatenate it into the string to avoid SQL injection, or handle it carefully using standard SQLite parameter binding or safe shell escaping if parameter binding isn't available in standard bash-sqlite wrappers).
6. The script must output the violations to standard output (stdout) in the following CSV format (including the header row exactly as shown):
`EmployeeName,SystemName,AccessDate,EmployeeClearance,RequiredClearance`

Sort the output by `AccessDate` in ascending order, then by `EmployeeName` in ascending order.

Ensure your script is executable (`chmod +x /home/user/generate_audit.sh`). Do not write the final output to a file inside the script; just print it to stdout so the automated auditing system can capture it.