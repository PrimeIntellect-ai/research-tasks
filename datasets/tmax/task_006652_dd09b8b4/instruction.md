You are a red-team operator crafting an evasion payload for a simulated assessment. You have discovered that an internal web application uses JWT for authentication and trusts an internal certificate authority. 

You have managed to exfiltrate the server's PKCS#12 keystore file located at `/home/user/server_keystore.p12`. The password for this keystore is `redteam123`.

Your objective is to craft a forged JWT payload that exploits an SQL injection vulnerability in the application's username field. 

Perform the following steps:
1. Extract the RSA private key from `/home/user/server_keystore.p12`.
2. Generate a JSON Web Token (JWT) signed with this private key using the `RS256` algorithm.
3. The JWT header must include the Key ID: `{"alg": "RS256", "kid": "internal-ca-01"}`.
4. The JWT payload must contain two claims:
   - `"role"`: set to `"admin"`
   - `"username"`: set to an SQL injection payload that will evaluate to true and bypass a basic WAF. The WAF blocks the characters `=`, ` `, and the word `OR`. You must use `/**/` for spaces, `LIKE` instead of `=`, and `||` for string concatenation or alternative logic to represent `admin' OR 1=1--`. Specifically, use exactly this payload string: `admin'/**/UNION/**/SELECT/**/1,2,3--`
5. Save the final encoded JWT string to a file named `/home/user/forged_payload.jwt`.
6. Write a Python script `/home/user/generate_payload.py` that fully automates steps 1-5, so the process can be audited.

Ensure all outputs are placed exactly where specified. You may use standard command-line tools (like `openssl`) and Python.