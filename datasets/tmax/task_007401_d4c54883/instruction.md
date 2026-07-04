You are a compliance analyst generating audit trails for an internal application. During a recent security review, a potential authentication vulnerability was flagged: the application's JWT verification library might accept tokens with the "none" algorithm (`alg: none`), bypassing signature validation.

Your task is to prove this vulnerability exists by forging an admin token and generating an audit trail.

Here are the details:
1. Parse the application logs located at `/home/user/auth_logs.txt` to find a legitimate, previously issued JWT for the user `admin`.
2. Analyze the decoded payload of the admin's JWT to understand the required claims.
3. Forge a new JWT that uses the "none" algorithm bypass. The payload must match the admin's original claims exactly. Ensure you use proper Base64Url encoding without padding (as required by the JWT standard).
4. Test your forged token by passing it as a command-line argument to the local authentication verification tool: `/home/user/auth_tool.py <your_forged_token>`
5. Create an audit trail:
   - Save your final forged token strictly as a single string inside `/home/user/audit_forged_jwt.txt`.
   - Save the exact standard output of `auth_tool.py` when run with your forged token into `/home/user/audit_report.txt`.

Ensure your forged token has the correct three-part JWT structure (`header.payload.signature`), where the signature is empty for the "none" algorithm.