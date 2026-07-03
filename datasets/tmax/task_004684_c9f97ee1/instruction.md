You are acting as a compliance analyst tasked with generating an automated security audit trail for a local internal appliance. 

An internal Go-based management server is running on `https://127.0.0.1:8443`. We suspect this appliance has several severe security misconfigurations. 

Your objective is to write a Go program at `/home/user/audit.go` that programmatically interfaces with this appliance, exploits a known JWT vulnerability to bypass authentication, and generates a compliance JSON report about the system's security posture.

Here is the intelligence we have gathered about the appliance:
1. **Certificate Chain:** The server runs over HTTPS using a custom internal Certificate Authority. The Root CA certificate is provided at `/home/user/ca.crt`. Your Go program must validate the server's certificate chain against this specific Root CA. Do not simply skip TLS verification (`InsecureSkipVerify: true` is prohibited).
2. **Authentication Bypass:** The appliance relies on JWT for authentication on its restricted `/api/ssh-config` endpoint. We suspect it is vulnerable to the `alg: "none"` attack. Your program must forge a JWT for the payload `{"role": "admin"}` using the "none" algorithm and pass it in the `Authorization: Bearer <token>` header to access the endpoint.
3. **Cookie Inspection:** When you successfully access the endpoint, the server will issue a `session_id` cookie. You must inspect the `Set-Cookie` headers to determine if this cookie is missing the `Secure` and `HttpOnly` flags.
4. **SSH Hardening Audit:** The response from `/api/ssh-config` will be a JSON object containing the appliance's current OpenSSH server configuration string in the `sshd_config` field. You must parse this configuration and determine if it violates our hardening baseline. Specifically, check if `PermitRootLogin` is set to `yes`, and if `PasswordAuthentication` is set to `yes`.

Your Go program (`/home/user/audit.go`) should perform all these checks automatically and output a compliance report strictly in JSON format to `/home/user/audit_report.json`.

The expected format of `/home/user/audit_report.json` is exactly as follows (use boolean `true` or `false` based on your findings):
```json
{
  "jwt_alg_none_vulnerable": true,
  "cookie_secure_flag_missing": true,
  "cookie_httponly_flag_missing": true,
  "ssh_root_login_permitted": true,
  "ssh_password_auth_permitted": true
}
```

Once you have written the code, compile and run your Go program to generate the required audit trail. Do not leave the task until the `/home/user/audit_report.json` file is successfully created with the correct boolean values based on the live server's state.