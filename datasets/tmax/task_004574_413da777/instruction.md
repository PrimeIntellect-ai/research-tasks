You are a network security engineer investigating a legacy authentication mechanism on a Linux server. A local CGI script is used to handle logins, and it relies on a proprietary compiled binary to validate credentials. Your goal is to reverse engineer the credentials, test the authentication flow, and document an open redirect vulnerability.

Perform the following steps:

1. **Binary Analysis**: Analyze the ELF binary located at `/home/user/auth_handler`. The developers hardcoded a default admin password in this binary. The encoded password string is prefixed with `PWD_` and the remainder of the string is base64 encoded. Extract and decode this password.

2. **Authentication Flow Testing**: The login flow is managed by a local CGI Bash script at `/home/user/login.cgi`. Execute this script, passing the decoded plaintext password as the very first command-line argument. 

3. **HTTP Header & Cookie Inspection**: If the password is correct, the script will output raw HTTP response headers simulating a successful login. Inspect this HTTP output. The server sets a session cookie and attempts to redirect the user.

4. **Reporting**: Extract the exact value of the `session_id` from the `Set-Cookie` header, and the exact redirect URL from the `Location` header. 
Create a file at `/home/user/report.txt` containing exactly two lines in the following format:
```
SESSION_ID=<extracted_session_id>
REDIRECT_URL=<extracted_redirect_url>
```
Make sure the file permissions of `/home/user/report.txt` allow the owner to read and write it.