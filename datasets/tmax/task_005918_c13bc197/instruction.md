You have been assigned as a security auditor to investigate a potentially compromised directory located at `/home/user/audit_target`. The system administrators suspect that a malicious user has left behind a backdoor, modified file permissions to maintain access, and logged in unauthorized.

Your objective is to perform a security audit using Python and bash commands, focusing on file permissions, reverse engineering, and log correlation.

Complete the following steps:

1. **Permission Audit:** 
   Identify all files within `/home/user/audit_target` (and its subdirectories) that are world-writable (i.e., the "others" write bit is set).

2. **Reverse Engineering:**
   The directory contains a compiled Python bytecode file at `/home/user/audit_target/bin/auth_helper.pyc`. The source code has been deleted. Disassemble or decompile this bytecode to extract a hardcoded fallback authentication token (a string variable that looks like a password or secret key).

3. **Log Correlation:**
   Examine the authentication log file located at `/home/user/audit_target/logs/auth.log`. Find the IP address of the attacker who successfully authenticated using the exact hardcoded token you discovered in the previous step.

4. **Reporting:**
   Compile your findings into a single JSON file located at `/home/user/audit_report.json`. The JSON must exactly match the following format and keys:
   ```json
   {
       "world_writable_files": [
           "/home/user/audit_target/path/to/file1.txt",
           "/home/user/audit_target/path/to/file2.sh"
       ],
       "hardcoded_token": "the_token_string_here",
       "attacker_ip": "192.168.x.x"
   }
   ```
   *Note: The `world_writable_files` list should contain the absolute paths of the files, sorted in alphabetical order.*