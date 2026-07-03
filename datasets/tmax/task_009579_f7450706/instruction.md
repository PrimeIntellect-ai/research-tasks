You are a security auditor tasked with investigating a potential security breach in a Go-based file upload microservice. We suspect an attacker has successfully exploited a path traversal vulnerability and uploaded executable scripts to the system.

You have been granted access to the server environment. Here is what you need to know:

1. **Log Analysis**: The microservice logs file upload requests to `/home/user/service/logs/server.log`. The log format is:
   `[TIMESTAMP] IP_ADDRESS - Token: <TOKEN> - UploadedPath: <FILEPATH>`
   You must use pattern matching to identify all upload attempts that contain path traversal sequences (specifically `../` or `..%2F`) in the `<FILEPATH>`.

2. **Token Validation**: Not all logged attempts were successful; some used expired or invalid authentication tokens. You must verify which of the malicious requests used a valid token. There is a Go program located at `/home/user/service/token_check.go`. You need to compile and use this program. It takes a token as a command-line argument (e.g., `./token_check <TOKEN>`) and exits with status code 0 if the token is valid, and status code 1 if it is invalid.

3. **Permission Auditing**: For every path traversal attempt that used a **valid** token, you must locate the corresponding file on the filesystem (the path in the log is relative to `/home/user/service/uploads/`, so a path of `../../scripts/malware.sh` would resolve to `/home/user/scripts/malware.sh`). 

4. **Identify Critical Risks**: Check the file permissions of these successfully uploaded malicious files. We are only looking for files that currently have **executable** permissions granted to the owner, group, or others, as these represent immediate remote code execution risks.

**Your Goal:**
Create a single text file at `/home/user/critical_findings.txt` containing the absolute paths of the maliciously uploaded files that successfully bypassed authentication (valid token) AND have executable permissions on the filesystem. List one absolute path per line.

Do not include files that were attempted with invalid tokens, do not include safe uploads, and do not include files that are not executable.