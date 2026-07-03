You are an incident responder investigating a compromised web server. The attackers left behind a stripped ELF binary at `/app/c2_decoder` that they used to obfuscate their malicious web request logs. 

We need to automate the detection of their attacks. Your task is to write an executable classification script at `/home/user/classifier` that can process an obfuscated log entry, decode it, and flag it as benign or malicious.

Your script must meet the following requirements:
1. It must accept exactly one argument: the absolute path to a file containing a single obfuscated log entry.
   Example: `/home/user/classifier /tmp/log_entry.txt`
2. It must use the stripped binary `/app/c2_decoder` to decode the file's contents. The binary reads from standard input and prints the decoded plaintext to standard output.
3. It must analyze the decoded plaintext log entry for web application vulnerabilities, specifically Cross-Site Scripting (XSS) and SQL Injection (SQLi) attempts.
4. It must print exactly the word `CLEAN` to standard output if the decoded request is benign, or `EVIL` if it contains XSS or SQLi payloads. Do not print anything else.
5. Make sure your script is executable (`chmod +x /home/user/classifier`). You may write the script in bash, Python, or any other language available on standard Linux systems.

Note: 
- XSS indicators include but are not limited to tags like `<script>`, event handlers like `onerror=`, or `javascript:` URIs.
- SQLi indicators include but are not limited to `UNION SELECT`, `' OR '1'='1`, and stacked queries (`; DROP TABLE`).
- The automated verification will test your script against a hidden corpus of clean and malicious payloads.