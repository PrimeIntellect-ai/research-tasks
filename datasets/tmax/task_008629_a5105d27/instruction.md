You are a penetration tester tasked with investigating a potential breach and remediating the vulnerability. 

A custom log analysis service running on the server has been parsing uploaded security logs to detect XSS injections. However, the service is suspected to have a path traversal vulnerability in its file handling logic. 

Here is your objective:

1. **Investigate the Logs:**
   You have access to the web server's access log at `/home/user/access.log`. Parse this log to identify the IP address of the attacker who successfully exploited the path traversal vulnerability to access the server's private SSH key (look for an HTTP 200 response for the SSH key file). 
   Write this exact IP address to a file at `/home/user/attacker_ip.txt`.

2. **Patch the C++ Vulnerability:**
   The vulnerable source code is located at `/home/user/service/uploader.cpp`. It takes a filename as a command-line argument, appends it to `/home/user/uploads/`, and scans it for XSS payloads (e.g., `<script>`).
   
   Fix the C++ code to prevent path traversal. You must modify the code such that:
   - It securely resolves the absolute path of the requested file (resolving any `..` or `.` components).
   - It verifies that the resolved canonical path strictly begins with `/home/user/uploads/`.
   - If the file attempts to escape the directory (or does not exist), the program MUST output exactly `Access Denied` to standard output and exit with status code `1`.
   - If the file is valid and inside the directory, it should proceed with the existing logic (opening the file and scanning for `<script>`).

3. **Compile the Fix:**
   Compile your patched version using `g++ -std=c++17 -o /home/user/service/uploader_fixed /home/user/service/uploader.cpp`.

Ensure that you do not change the existing XSS scanning logic, only the file path validation. All files and directories are within `/home/user`.