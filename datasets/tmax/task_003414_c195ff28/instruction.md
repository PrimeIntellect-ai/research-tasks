You are a DevSecOps engineer enforcing security policy as code. We need to build a lightweight, custom static analyzer and log inspector in C++ to run in our CI/CD pipeline. 

There are two files that need to be analyzed:
1. `/home/user/audit_data/source_code.txt` (a snippet of our web application's backend code)
2. `/home/user/audit_data/auth.log` (a sample of authentication logs)

Your task is to write a C++ program at `/home/user/policy_scanner.cpp` that scans these files and generates a security report at `/home/user/scan_results.txt`.

The program must implement the following policies using pattern matching (`std::regex` or string searching) and basic algorithmic logic:

**Policy 1: Detect SQL Injection Vulnerabilities**
Scan `source_code.txt` line by line. Flag any line that contains the word `SELECT` followed by `WHERE`, and also contains a string concatenation using the `+` operator.
Log the finding in the report as: `VULN: SQLi found on line X` (where X is the 1-based line number).

**Policy 2: Detect Cross-Site Scripting (XSS) Vulnerabilities**
Scan `source_code.txt` line by line. Flag any line that contains an HTML tag (e.g., `<h1>`, `<div>` - any `<` followed by letters/numbers and `>`) AND concatenates a variable using the `+` operator on the same line.
Log the finding in the report as: `VULN: XSS found on line Y`

**Policy 3: Detect Authentication Brute-Force**
Scan `auth.log`. Each line is formatted as `IP_ADDRESS - STATUS`. Keep track of the number of `FAILED LOGIN` events per IP address. If an IP address has strictly more than 3 `FAILED LOGIN` events, flag it.
Log the finding in the report as: `ALERT: Brute force detected from IP_ADDRESS` (print this only once per flagged IP).

**Execution:**
Once you have written `/home/user/policy_scanner.cpp`:
1. Compile it using: `g++ -std=c++17 /home/user/policy_scanner.cpp -o /home/user/policy_scanner`
2. Run it: `/home/user/policy_scanner`
3. Ensure it writes the output exactly as specified to `/home/user/scan_results.txt`, with each finding on a new line. The order of lines in the output should be SQLi findings first, XSS findings second, and Brute force alerts last.