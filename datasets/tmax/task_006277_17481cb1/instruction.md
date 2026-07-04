You are a security engineer tasked with rotating the master credential for a local legacy microservice. The engineer who originally set up the service has left, and the documentation is missing the current administration token and the recovery PIN.

The microservice is running locally on `http://127.0.0.1:5000`. 
It has an endpoint `/admin/rotate_secret` which accepts POST requests.

To successfully rotate the secret, you must:
1. **Bypass Authentication**: The endpoint requires a JWT in the `Authorization: Bearer <token>` header. The token must have the claim `{"role": "admin"}`. You do not have the secret key to sign this token, but a recent audit noted that the JWT implementation is vulnerable to an "algorithm substitution" attack and will accept tokens with the algorithm set to `none`. Generate a forged token using Python to bypass this.
2. **Brute-force the Recovery PIN**: The POST request must include a JSON payload with a `"recovery_pin"` (a 4-digit string from `"0000"` to `"9999"`) and a `"new_secret"` (set this to `"secure_new_admin_123"`). You must write a script to brute-force the 4-digit PIN until the server accepts the request.
3. **Capture the Confirmation**: Upon success, the server will return a JSON response containing a `"confirmation"` field. Extract this confirmation value and save it exactly as plain text in `/home/user/rotation_success.txt`.
4. **Draft a WAF Rule**: To prevent external exploitation of this endpoint before it can be patched, draft a basic Web Application Firewall (WAF) rule policy. Create a JSON file at `/home/user/waf_rules.json` with exactly the following structure:
```json
{
  "rules": [
    {
      "endpoint": "/admin/rotate_secret",
      "allowed_ips": ["127.0.0.1"],
      "action": "drop_others"
    }
  ]
}
```

Constraints:
- Do not use any external network requests or third-party cracking tools; write a Python script to perform the token generation and brute-forcing.
- The WAF rule file must strictly match the provided JSON format.