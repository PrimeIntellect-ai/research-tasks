You are a security auditor hired to review and secure a custom, lightweight Bash-based web application. The application deployment relies on a setup script that creates a web directory, writes configuration files, and launches a simple HTTP server using `socat`.

The environment currently has a directory containing the application code:
- `/home/user/server_setup.sh`: The deployment and server execution script.
- `/home/user/src/cgi-bin/greet.sh`: A Bash CGI script served by the application.

Your task is to identify and remediate security vulnerabilities in these scripts based on the following requirements:

1. **File Permission & Access Control**: 
   The `server_setup.sh` script currently writes a sensitive file `/home/user/www/config/db_secret.key`. This file is currently being created with insecure default permissions (world-readable). Modify `server_setup.sh` so that when it creates this file, it explicitly sets the file permissions to `600` (read and write for the owner only).

2. **HTTP Header Inspection & Security**:
   The custom `socat` HTTP response in `server_setup.sh` lacks essential security headers. Modify the HTTP response block within `server_setup.sh` to include the following HTTP headers:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`

3. **Injection Analysis & Remediation**:
   The `/home/user/src/cgi-bin/greet.sh` script takes a URL parameter (`name`) from the `QUERY_STRING` environment variable and improperly evaluates it, leading to a Command Injection vulnerability. The script currently uses `eval` or command substitution unsafely. Modify `/home/user/src/cgi-bin/greet.sh` to safely parse the `name` parameter without executing arbitrary commands. Ensure that it still outputs the value of the `name` parameter in the HTML response, but safely sanitized (e.g., stripping out characters like `;`, `|`, `$`, `` ` ``, and `&`).

4. **Audit Report**:
   Create a file at `/home/user/audit_report.json` summarizing your findings. The JSON file must strictly follow this format:
   ```json
   {
     "vulnerabilities_fixed": [
       "Insecure File Permissions",
       "Missing Security Headers",
       "Command Injection"
     ],
     "db_secret_permission": "600",
     "added_headers": ["X-Content-Type-Options", "X-Frame-Options"]
   }
   ```

Do not change the fundamental architecture of the server (it must still use `socat` and Bash), just patch the security flaws.