You are a security auditor tasked with performing a quick automated security and permissions check on a lightweight web application directory. 

Write a Bash script at `/home/user/audit.sh` that scans the directory `/home/user/webapp/` and checks for specific security vulnerabilities and misconfigurations. 

Your script must implement the following checks:
1. **File Permission Check:** Find any files within the directory that are world-writable (others have write permission). Flag these as `World_Writable`.
2. **CSP and XSS Check:** Scan all `.html` and `.js` files. If a file contains the exact case-sensitive string `<script` but does NOT contain either the string `nonce=` or `integrity=`, flag it as `CSP_XSS_Risk`.
3. **Injection Check:** Scan all `.php` files. If a file contains the exact case-sensitive string `eval(`, flag it as `Injection_Risk`.

**Output Requirements:**
The script must generate a CSV report at `/home/user/audit_report.csv`.
Each line in the CSV must be formatted exactly as:
`[Absolute_File_Path],[Issue_Type]`

For example:
`/home/user/webapp/bad.php,Injection_Risk`
`/home/user/webapp/bad.php,World_Writable`
`/home/user/webapp/unsafe.html,CSP_XSS_Risk`

If a file has multiple issues (e.g., a PHP file that is world-writable and contains an eval), it should have a separate line for each issue. 
Finally, your script must sort the output file alphabetically so the resulting CSV is deterministic.

Run your script once it is written to produce the `/home/user/audit_report.csv` file.