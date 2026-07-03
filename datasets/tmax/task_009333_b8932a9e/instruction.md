As a compliance analyst, you are auditing an internal authentication service written in C. During your analysis, you discovered that the service's token validation logic contains a critical vulnerability: it mirrors a well-known JWT flaw where tokens specifying the algorithm "none" (`"alg":"none"`) are accepted without signature verification. 

Your objective is to patch this vulnerability, compile the binary, and generate an audit trail of recent access attempts.

Here are your instructions:

1. **Patch the Vulnerability**: You have been provided the source code of the service at `/home/user/auth_server.c`. 
   Analyze the code to find the flaw. Modify the code so that if the token header indicates `"alg":"none"` (or its exact Base64URL equivalent used in the code), the program immediately prints `REJECTED: INSECURE_ALG` to standard output and exits with a status code of `1`. 

2. **Compile the Binary**: Compile your patched code into an ELF executable located at `/home/user/auth_server`. Use `gcc` with standard options.

3. **Generate the Audit Trail**: You have a log of recent tokens in `/home/user/tokens.txt`. Each line is formatted as `TokenID:TokenString`.
   Write a script or use shell commands to pass each `TokenString` as the first command-line argument to your patched `/home/user/auth_server`.
   Create an audit log file at `/home/user/audit_trail.log`. For each token, append a line in the exact format: `[TokenID] <OUTPUT>` (where `<OUTPUT>` is the stdout printed by the `auth_server`).

4. **Identify the Exploit**: Review your audit trail to find the `TokenID` of the malicious token that attempted to exploit the "alg=none" vulnerability. Write ONLY this `TokenID` (e.g., `TKN-99`) to the file `/home/user/exploit_id.txt`.

Ensure all files are placed in `/home/user/` and have the exact names specified.